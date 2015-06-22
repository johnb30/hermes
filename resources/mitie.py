#!flask/bin/python
from __future__ import unicode_literals
import os
import sys
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


class MitieAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('content', type=unicode, location='json')
        args = self.reqparse.parse_args()  # setup the request parameters
        self.content = args['content']
        self.result = {}
        super(MitieAPI, self).__init__()

    def post(self):
        app.logger.info('Started processing content.')
        self.call_mitie()
        app.logger.info('Finished processing content.')
        return self.result, 201

    def call_mitie(self):
        result_key = 'MITIE'
        mitie_payload = {'content': self.content}  # .encode('utf-8')}

        # get MITIE address
        mitie_ip = os.environ['MITIE_PORT_5001_TCP_ADDR']
        mitie_url = 'http://{}:{}'.format(mitie_ip, '5001')
        # hit MITIE containter
        try:
            mitie_r = requests.post(mitie_url, json=mitie_payload)
            mitie_r.raise_for_status()
            try:
                mitie_r = mitie_r.json()
                for key in mitie_r.keys():
                    mitie_r[key] = json.loads(mitie_r[key])
            except Exception as e:
                app.logger.error(e)
                mitie_r = {}
        except requests.exceptions.HTTPError as e:
            app.logger.error(e)
            mitie_r = {}

        self.result[result_key] = mitie_r
