#!flask/bin/python
from __future__ import unicode_literals
import os
import sys
import json
import logging
import requests
import geolocation
from threading import Thread
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from flask import Flask
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


class CliffAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('content', type=unicode, location='json')
        args = self.reqparse.parse_args()  # setup the request parameters
        self.content = args['content']
        self.result = {}
        super(CliffAPI, self).__init__()


    def post(self):
        logger.info('Started processing content.')
        self.call_cliff
        logger.info('Finished processing content.')
        return self.result, 201

    def call_cliff(self):
        result_key = 'CLIFF'
        cliff_ip = os.environ['CLIFF_PORT_8080_TCP_ADDR']
        cliff_url = 'http://{}:{}/CLIFF-2.0.0/parse/text'.format(cliff_ip,
                                                                 '8080')
        cliff_payload = {'q': self.content}  # .encode('utf-8')}
        try:
            cliff_t = requests.get(cliff_url, params=cliff_payload)
        except requests.exceptions.RequestException as e:
            logger.error(e)
            cliff_r = {}
        try:
            cliff_t = cliff_t.json()
            if cliff_t:
                cliff_r = geolocation.process_cliff(cliff_t)
            else:
                cliff_r = cliff_t
        except Exception as e:
            logger.error(e)
            cliff_r = {}

        self.result[result_key] = cliff_r
