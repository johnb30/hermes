import logging
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from flask import Flask
from flask.ext.restful import Api
from resources.hermes import HermesAPI

formatter = logging.Formatter('%(levelname)s %(asctime)s %(filename)s: %(message)s')
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(formatter)
app.logger.addHandler(ch)
app.logger.setLevel(logging.INFO)

app = Flask(__name__)
api = Api(app)

api.add_resource(HermesAPI, '/hermes')

if __name__ == '__main__':
    app.logger.info('Starting Hermes.')
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    IOLoop.instance().start()
