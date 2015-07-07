#!flask/bin/python
import logging
from flask import Flask
from flask.ext.restful import Api, Resource, reqparse
from flask.ext.restful.representations.json import output_json
from gensim import models
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

output_json.func_globals['settings'] = {'ensure_ascii': False, 'encoding':'utf8'}

app = Flask(__name__)
api = Api(app)

logging.basicConfig(format='%(levelname)s %(asctime)s %(filename)s %(lineno)d: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

stopwords = stopwords.words('english')
stemmer = PorterStemmer()

tops_mapping = {13: 'Control', 41: 'ISIL/fighting', 19: 'Syria', 11: 'U.S.',
                37: 'Rebels', 9: 'Misc', 16: 'Cities', 38: 'Kobani', 22: 'Bomb',
                18: 'Women/children', 2: 'Turkey', 21: 'Government',
                6: 'Kurds', 4: 'Diplomacy', 43: 'Aid', 26: 'Jordan',
                29: 'Diplomacy', 33: 'Human rights', 14: 'Opposition',
                5: 'Videos', 27: 'Fighting groups',  1: 'Arab/Syria',
                40: 'Airstrike', 32: 'Hostages', 28: 'Iraq', 48: 'Oil',
                20: 'Governance', 15: 'Yazidi', 31: 'Misc', 3: 'Assad',
                46: 'Chemical Weapons', 30: 'ISIL', 23: 'Conflict', 39: 'Aid',
                44: 'Saudi Arabia', 24: 'Misc', 36: 'Lebanon', 7: 'Syria',
                12: 'ISIL', 49: 'Muslim', 25: 'Misc', 47: 'Misc', 45: 'Rebels',
                8: 'Jordan/Coalition', 34: 'Misc', 10: 'Kurdish', 0: '?',
                35: 'Pilot', 17: '?', 42: 'Airstrike'}

model = models.utils.SaveLoad.load('/src/control_model.model')
dictionary = models.utils.SaveLoad.load('/src/syr_irq_dict.model')


class TopicsAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('content', type=unicode, location='json')
        super(TopicsAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        sentence = args['content'] #.encode('utf-8')
        content = [stemmer.stem(word) for word in sentence.lower().split() if word
                not in stopwords]

        logger.info('Started processing content.')
        try:
            out = self.process(content)
            to_return = self.postprocess(out)
            logger.info('Finished processing content.')
        except Exception as e:
            logger.info(e)
            to_return = {}

        return to_return

    def process(self, content):
        doc = dictionary.doc2bow(content)
        out = model[doc]
        return out

    def postprocess(self, out):
        doc_max = 0.0
        max_index = ''
        for top in out:
            if abs(float(top[1])) > doc_max:
                doc_max = float(top[1])
                max_index = top[0]
        max_top_string = tops_mapping[max_index]

        tops_strings = []
        for top in out:
            new_tuple = (tops_mapping[top[0]], top[1])
            tops_strings.append(new_tuple)

        res = {'topics': out, 'topic_strings': tops_strings,
               'highest_topic_index': max_index, 'highest_topic_string':
               max_top_string}
        return res

api.add_resource(TopicsAPI, '/')

if __name__ == '__main__':
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5002)
    IOLoop.instance().start()
