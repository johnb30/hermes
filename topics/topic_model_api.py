import json
from gensim import models
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

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

model = models.utils.SaveLoad.load('control_model.model')
dictionary = models.utils.SaveLoad.load('syr_irq_dict.model')


def get_topics(sentence):
    content = [stemmer.stem(word) for word in sentence.lower().split() if word
               not in stopwords]
    doc = dictionary.doc2bow(content)
    out = model[doc]

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

    to_return = {'topics': out, 'topic_strings': tops_strings,
                 'highest_topic_index': max_index,
                 'highest_topic_string': max_top_string}
    return json.dumps(to_return)