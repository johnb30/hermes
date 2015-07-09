import os
import logging
import requests
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from flask import Flask, jsonify, make_response
from flask.ext.restful import Api
from resources.hermes import HermesAPI
from resources.mitie import MitieAPI
from resources.cliff import CliffAPI
from resources.joshua import JoshuaAPI
from resources.topics import TopicsAPI
from resources.mordecai import MordecaiAPI

app = Flask(__name__)
api = Api(app)

api.add_resource(HermesAPI, '/hermes')
api.add_resource(MitieAPI, '/hermes/mitie')
api.add_resource(CliffAPI, '/hermes/cliff')
api.add_resource(TopicsAPI, '/hermes/topics')
api.add_resource(MordecaiAPI, '/hermes/mordecai')
api.add_resource(JoshuaAPI, '/hermes/joshua')


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s %(asctime)s %(filename)s %(lineno)d: %(message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    app.logger.info('Starting Hermes.')
    app.logger.info('Checking container links.')
    try:
        mitie_ip = os.environ['MITIE_PORT_5001_TCP_ADDR']
        app.logger.info('Successfully reached MITIE on port 5001')
    except KeyError:
        app.logger.info('Unable to reach MITIE on port 5001')
    try:
        topics_ip = os.environ['TOPICS_PORT_5002_TCP_ADDR']
        app.logger.info('Successfully reached Topics on port 5002')
    except KeyError:
        app.logger.info('Unable to reach Topics on port 5002')
    try:
        cliff_ip = os.environ['CLIFF_PORT_8080_TCP_ADDR']
        app.logger.info('Successfully reached CLIFF on port 8080')
    except KeyError:
        app.logger.info('Unable to reach CLIFF on port 8080')
    try:
        joshua_ip = os.environ['JOSHUA_PORT_5009_TCP_ADDR']
        app.logger.info('Successfully reached JOSHUA on port 5009')
    except KeyError:
        app.logger.info('Unable to reach JOSHUA on port 5009')
    headers = {'Content-Type': 'application/json'}
    mordecai_ip = '0.0.0.0'
    r = requests.get('http://{}:8999/places'.format(mordecai_ip),
                     headers=headers)
    if r.status_code == 200:
        app.logger.info('Successfully reached Mordecai at {}'.format(mordecai_ip))
    else:
        app.logger.info('Unable to reach Mordecai at {}'.format(mordecai_ip))

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    IOLoop.instance().start()
