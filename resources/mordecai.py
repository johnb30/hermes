#!flask/bin/python
from __future__ import unicode_literals
import json
import logging
import requests
import geolocation
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


class MordecaiAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('content', type=unicode, location='json')
        args = self.reqparse.parse_args()  # setup the request parameters
        self.content = args['content']
        self.result = {}
        super(MordecaiAPI, self).__init__()


    def post(self):
        logger.info('Started processing content.')
        self.call_mordecai()
        logger.info('Finished processing content')
        return self.result, 201

    def call_mordecai(self):
        result_key = 'mordecai'
        mordecai_ip = '0.0.0.0'
        mordecai_url = 'http://{}:{}/places'.format(mordecai_ip, '8999')

        try:
            mordecai_headers = {'Content-Type': 'application/json'}
            mordecai_payload = json.dumps({'text': self.content})
            mordecai_t = requests.post(mordecai_url, data=mordecai_payload,
                                       headers=mordecai_headers).json()
        except requests.exceptions.RequestException as e:
            logger.error(e)
            mordecai_t = {}
        if mordecai_t:
            mordecai_r = geolocation.process_mordecai(mordecai_t)
        else:
            mordecai_r = mordecai_t

        self.result[result_key] = mordecai_r
