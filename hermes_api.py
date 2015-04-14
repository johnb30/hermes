#!flask/bin/python
from __future__ import unicode_literals
import os
import json
import requests
from flask import Flask, jsonify, make_response
from flask.ext.restful import Api, Resource, reqparse
from flask.ext.httpauth import HTTPBasicAuth

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


class HermesAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('content', type=str, location='json')
        super(HermesAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args() # setup the request parameters
        mitie_payload = {'content': args['content'].encode('utf-8')}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        mitie_ip = os.environ['MITIE_PORT_5001_TCP_ADDR'] # get MITIE endpoint
        mitie_url = 'http://' + mitie_ip + ':5001'
        try:
            mitie_r = requests.post(mitie_url, json=mitie_payload) # hit MITIE containter
        except:
            mitie_r = {'MITIE request failed'}

        cliff_ip = os.environ['CLIFF_PORT_8080_TCP_ADDR']
        cliff_url = "http://{}:{}/CLIFF-2.0.0/parse/text".format(cliff_ip, '8080')
        cliff_payload = {'q': args['content'].encode('utf-8')}
        try:
            cliff_r = requests.get(cliff_url, params=cliff_payload)
        except:
            cliff_r = {'CLIFF request failed'}

#       topics_ip =
#       topics_url =
#       topics_r =

        return {'MITIE': mitie_r.json(), 'CLIFF': cliff_r.json()}, 201

api.add_resource(HermesAPI, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
