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


class JoshuaAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('content', type=unicode, location='json')
        args = self.reqparse.parse_args()  # setup the request parameters
        self.content = args['content']
        self.result = {}
        super(JoshuaAPI, self).__init__()

    def post(self):
        logger.info('Started processing content.')
        self.call_joshua()
        logger.info('Finished processing content')
        return self.result, 201

    def call_joshua(self):
        joshua_payload = {'text': self.arabic_content}

        try:
            joshua_ip = os.environ['JOSHUA_PORT_5009_TCP_ADDR']
            joshua_url = 'http://{}:{}'.format(joshua_ip, '5009')
            logger.info('Sending to joshua.')
            joshua_r = requests.post(joshua_url,
                                     json=joshua_payload).json()
            joshua_r = json.loads(joshua_r)
        except KeyError:
            logger.warning('Unable to reach joshua container. Returning nothing.')
            joshua_r = {}
        return joshua_r
