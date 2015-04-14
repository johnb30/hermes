#!flask/bin/python
from __future__ import unicode_literals
import sys
import os

parent = os.path.dirname(os.path.realpath(__file__))
sys.path.append('/MITIE/mitielib')

import re
import json
from flask import Flask
from flask.ext.restful import Api, Resource, reqparse
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from mitie import *

app = Flask(__name__)
api = Api(app)

ner = named_entity_extractor('/MITIE/MITIE-models/english/ner_model.dat')


class MitieAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('content', type=str, location='json')
        super(MitieAPI, self).__init__()

    def post(self):
        out = []
        args = self.reqparse.parse_args()
        content = args['content'].encode('utf-8')
        tokens = tokenize(content)
        entities = ner.extract_entities(tokens)
        for e in entities:
            range = e[0]
            start = range.__reduce__()[1][0]
            stop = range.__reduce__()[1][1]
            tag = e[1]
            score = e[2]
            entity_text = " ".join(tokens[i] for i in range)
            out.append({u'tag': tag, u'entity_text': entity_text, u'start':
                        start, u'stop': stop, u'score': score})
        cleaned_tokens = []
        stopwords = ["", "a", "an", "and", "are", "as", "at", "be", "but", "by",
                     "for", "if", "in", "into", "is", "it", "no", "not", "of",
                     "on", "or", "s", "such", "t", "that", "the", "their",
                     "then", "there", "these", "they", "this", "to", "was",
                     "will", "with"]
        for t in tokens:
            t = re.sub("\W", "", t).lower()
            if t not in stopwords:
                cleaned_tokens.append(t)
        for e in reversed(entities):
            range = e[0]
            tag = e[1]
            newt = tokens[range[0]]
            if len(range) > 1:
                for i in range:
                    if i != range[0]:
                        newt += str(' ') + tokens[i]
                        newt = str('<span class="mitie-') + tag  + str('">') + newt + str('</span>')
                        tokens = tokens[:range[0]] + [newt] + tokens[(range[-1] + 1):]
        html = str(' ').join(tokens)
        htmlu = unicode(html.decode("utf-8"))
        return {"entities": json.dumps(out), "cleaned_tokens":
                json.dumps(cleaned_tokens), "html": json.dumps(htmlu)}, 201

api.add_resource(MitieAPI, '/')

if __name__ == '__main__':
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5001)
    IOLoop.instance().start()
