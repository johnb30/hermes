#!flask/bin/python
from __future__ import unicode_literals
import os
import json
import logging
import requests
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


class TopicsAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('content', type=unicode, location='json')
        args = self.reqparse.parse_args()  # setup the request parameters
        self.content = args['content']
        self.result = {}
        super(TopicsAPI, self).__init__()

    def post(self):
        logger.info('Started processing content.')

        try:
            topics_ip = os.environ['TOPICS_PORT_5002_TCP_ADDR']
            topics_url = 'http://{}:{}'.format(topics_ip, '5002')
            topics_payload = {'content': self.content}
            topics_r = requests.post(topics_url, json=topics_payload).json()
            topics_r = json.loads(topics_r)
        except Exception as e:
            logger.error(e)
            topics_r = {}

        self.result['topic_model'] = topics_r

        logger.info('Finished processing content.')
        return self.result, 201
