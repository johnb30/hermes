#!flask/bin/python
from __future__ import unicode_literals
import os
import json
import langid
import logging
import requests
import geolocation
from threading import Thread
from flask import jsonify, make_response
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.restful import Resource, reqparse
from flask.ext.restful.representations.json import output_json

output_json.func_globals['settings'] = {'ensure_ascii': False,
                                        'encoding': 'utf8'}

logger = logging.getLogger('__main__')
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'user':
        return 'text2features'
    return None


@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the
    # default auth dialog
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)


class HermesAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('content', type=unicode, location='json')
        self.reqparse.add_argument('lang', location='json')
        langid.set_languages(['ar', 'en'])
        super(HermesAPI, self).__init__()

    def post(self):
        logger.info('Started processing content.')
        self.result = {}

        args = self.reqparse.parse_args()  # setup the request parameters
        if args['lang'] == 'ar':
            self.content = ''
            self.arabic_content = args['content']
        elif args['lang'] == 'en':
            self.content = args['content']
            self.arabic_content = ''
        elif not args['lang']:
            lang = langid.classify(args['content'])[0]
            if lang == 'ar':
                self.content = ''
                self.arabic_content = args['content']
            elif lang == 'en':
                self.content = args['content']
                self.arabic_content = ''

        if self.arabic_content:
            self.content = self.call_joshua()
            self.result['joshua'] = self.content
        else:
            self.result['joshua'] = ''

        funcs = [self.call_cliff, self.call_mitie, self.call_mordecai]
        threads = [Thread(target=f) for f in funcs]
        [t.start() for t in threads]
        [t.join() for t in threads]

        try:
            if not self.result['CLIFF']:
                logger.info('No CLIFF info. Skipping topic model.')
                topics_d = {}
            else:
                apply_topic = ('SYR' in self.result['CLIFF']['country_vec'] or
                               'IRQ' in self.result['CLIFF']['country_vec'])
                if apply_topic:
                    topics_d = self.call_topics()
                else:
                    topics_d = {}
            self.result['topic_model'] = topics_d
        except Exception as e:
            logger.error(e)
            topics_d = {}
            self.result['topic_model'] = topics_d

# Bye for now CoreNLP
#        stanford_ip = os.environ['STANFORD_PORT_5003_TCP_ADDR']
#        server = jsonrpclib.Server('http://' + stanford_ip + ":5003")
#        stanford_r = loads(server.parse(args['content']))
        stanford_r = {}
        self.result['stanford'] = stanford_r

        logger.info('Finished processing content.')
        return self.result, 201

    def call_mitie(self):
        result_key = 'MITIE'
        mitie_payload = {'content': self.content}  # .encode('utf-8')}

        # get MITIE address
        try:
            mitie_ip = os.environ['MITIE_PORT_5001_TCP_ADDR']
            mitie_url = 'http://{}:{}'.format(mitie_ip, '5001')
            # hit MITIE containter
            try:
                logger.info('Sending to MITIE')
                mitie_r = requests.post(mitie_url, json=mitie_payload)
                mitie_r.raise_for_status()
                mitie_r = mitie_r.json()
            except Exception as e:
                logger.error(e)
                mitie_r = {}

        except KeyError:
            logger.warning('Unable to reach MITIE container. Returning nothing.')
            mitie_r = {}

        self.result[result_key] = mitie_r

    def call_cliff(self):
        result_key = 'CLIFF'

        try:
            cliff_ip = os.environ['CLIFF_PORT_8080_TCP_ADDR']
            cliff_url = 'http://{}:{}/CLIFF-2.0.0/parse/text'.format(cliff_ip,
                                                                     '8080')
            cliff_payload = {'q': self.content}  # .encode('utf-8')}
            try:
                logger.info('Sending to CLIFF.')
                cliff_t = requests.get(cliff_url, params=cliff_payload)
                cliff_t = cliff_t.json()
                if cliff_t:
                    cliff_r = geolocation.process_cliff(cliff_t)
                else:
                    cliff_r = cliff_t
            except Exception as e:
                logger.error(e)
                cliff_r = {}

        except KeyError:
            logger.warning('Unable to reach CLIFF container. Returning nothing.')
            cliff_r = {}

        self.result[result_key] = cliff_r

    def call_mordecai(self):
        result_key = 'mordecai'
        mordecai_ip = '0.0.0.0'
        mordecai_url = 'http://{}:{}/places'.format(mordecai_ip, '8999')

        try:
            logger.info('Sending to Mordecai.')
            mordecai_headers = {'Content-Type': 'application/json'}
            mordecai_payload = json.dumps({'text': self.content})
            mordecai_t = requests.post(mordecai_url, data=mordecai_payload,
                                       headers=mordecai_headers).json()
            if mordecai_t:
                mordecai_r = geolocation.process_mordecai(mordecai_t)
            else:
                mordecai_r = {}
        except requests.exceptions.RequestException as e:
            logger.error(e)
            mordecai_r = {}

        self.result[result_key] = mordecai_r

    def call_topics(self):
        topics_payload = {'content': self.content}

        try:
            topics_ip = os.environ['TOPICS_PORT_5002_TCP_ADDR']
            topics_url = 'http://{}:{}'.format(topics_ip, '5002')
            logger.info('Sending to the topic model.')
            topics_r = requests.post(topics_url,
                                     json=topics_payload).json()
        except KeyError:
            logger.warning('Unable to reach Topics container. Returning nothing.')
            topics_r = {}
        return topics_r

    def call_joshua(self):
        joshua_payload = json.dumps({'text': self.arabic_content})
        joshua_headers = {'Content-Type': 'application/json'}

        try:
            joshua_ip = os.environ['JOSHUA_PORT_5009_TCP_ADDR']
            joshua_url = 'http://{}:{}/joshua/translate'.format(joshua_ip,
                                                                '5009')
            logger.info('Sending to joshua.')
            joshua_r = requests.get(joshua_url, data=joshua_payload,
                                    headers=joshua_headers).json()
            joshua_r = joshua_r.replace('\n', '')
            logger.info(joshua_r)
        except KeyError:
            logger.warning('Unable to reach joshua container. Returning nothing.')
            joshua_r = {}
        return joshua_r
