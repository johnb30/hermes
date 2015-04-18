#!flask/bin/python
from __future__ import unicode_literals
import os
import json
import requests
import geolocation
import jsonrpclib
from simplejson import loads
from flask import Flask, jsonify, make_response
from flask.ext.restful import Api, Resource, reqparse
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.restful.representations.json import output_json
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

output_json.func_globals['settings'] = {'ensure_ascii': False, 'encoding':'utf8'}

app = Flask(__name__)
api = Api(app)
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


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


class HermesAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('content', type=unicode, location='json')
        super(HermesAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()  # setup the request parameters
        mitie_payload = {'content': args['content']} #.encode('utf-8')}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        mitie_ip = os.environ['MITIE_PORT_5001_TCP_ADDR']  # get MITIE address
        mitie_url = 'http://{}:{}'.format(mitie_ip, '5001')
        # hit MITIE containter
        mitie_r = requests.post(mitie_url, json=mitie_payload).json()

        cliff_ip = os.environ['CLIFF_PORT_8080_TCP_ADDR']
        cliff_url = 'http://{}:{}/CLIFF-2.0.0/parse/text'.format(cliff_ip,
                                                                 '8080')
        cliff_payload = {'q': args['content']} #.encode('utf-8')}
        cliff_t = requests.get(cliff_url, params=cliff_payload).json()
        if cliff_t:
            cliff_r = geolocation.process_cliff(cliff_t)
        else:
            cliff_r = cliff_t

        if 'SYR' in cliff_r['country_vec'] or 'IRQ' in cliff_r['country_vec']:
            topics_ip = os.environ['TOPICS_PORT_5002_TCP_ADDR']
            topics_url = 'http://{}:{}'.format(topics_ip, '5002')
            topics_payload = {'content': args['content']} #.encode('utf-8')}
            topics_r = requests.post(topics_url, json=topics_payload).json()
        else:
            topics_r = json.dumps({})

        stanford_ip = os.environ['STANFORD_PORT_5003_TCP_ADDR']
        server = jsonrpclib.Server('http://' + stanford_ip + ":5003")
        stanford_r = loads(server.parse(args['content']))

        return {'MITIE': mitie_r, 'CLIFF': cliff_r, 'topic_model': topics_r,
                'stanford': stanford_r}, 201

api.add_resource(HermesAPI, '/')

if __name__ == '__main__':
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    IOLoop.instance().start()
