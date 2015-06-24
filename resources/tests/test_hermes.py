from ..hermes import HermesAPI


def test_mordecai():
    a = HermesAPI()
    a.result = {}
    a.content = 'John Kerry reported that ISIL attacked Aleppo.'
    a.call_mordecai()
    result_morty = a.result['mordecai']
    expect = {'focus_countries': {u'SYR': 1}, 'country_vec': [u'SYR'],
              'locations': [{u'lat': 36.20124, u'searchterm': u'Aleppo',
              u'lon': 37.16117, u'countrycode': u'SYR', u'placename': u'Aleppo'}]}
    assert result_morty == expect


def test_mitie():
    a = HermesAPI()
    a.result = {}
    a.content = 'John Kerry reported that ISIL attacked Aleppo.'
    a.call_mitie()
    result_mitie = a.result['MITIE']
    expect = {u'entities': u'[{"start": 0, "entity_text": "John Kerry", "tag": "PERSON", "stop": 2, "score": 1.4700564914291707}, {"start": 4, "entity_text": "ISIL", "tag": "ORGANIZATION", "stop": 5, "score": 0.2995116136279095}, {"start": 6, "entity_text": "Aleppo", "tag": "LOCATION", "stop": 7, "score": 0.9780241497679095}]',
                u'html': u'"<span class=\\"mitie-PERSON\\">John Kerry</span> reported that ISIL attacked Aleppo ."'}
    assert result_mitie == expect


def test_cliff():
    a = HermesAPI()
    a.result = {}
    a.content = 'John Kerry reported that ISIL attacked Aleppo.'
    a.call_cliff()
    result_cliff = a.result['CLIFF']
    expect = {u'cliff_orgs': [],
              u'cliff_people': [u'John Kerry'],
              u'country_vec': [u'SYR'],
              u'focus_cities': [{u'countryCode': u'SYR',
                                 u'lat': 36.20124,
                                 u'lon': 37.16117,
                                 u'name': u'Aleppo',
                                 u'stateName': u'Aleppo Governorate'}],
              u'focus_countries': [{u'countryCode': u'SYR',
                                    u'lat': 35.0,
                                    u'lon': 38.0,
                                    u'name': u'Syrian Arab Republic'}],
              u'focus_states': [{u'countryCode': u'SYR',
                                 u'lat': 36.25,
                                 u'lon': 37.61667,
                                 u'name': u'Aleppo Governorate',
                                 u'stateCode': u'09'}],
              u'stateVec': [u'Aleppo Governorate']}
    assert result_cliff == expect


def test_topics():
    a = HermesAPI()
    a.result = {}
    a.content = 'John Kerry reported that ISIL attacked Aleppo.'
    a.call_topics()
    result_topics = a.result['topic_model']
    expect = {"topics": [[4, 0.33245449113625491], [12, 0.30518845761137631], [29, 0.22807133696665638]], "highest_topic_string": "Diplomacy", "highest_topic_index": 4, "topic_strings": [["Diplomacy", 0.33245449113625491], ["ISIL", 0.30518845761137631], ["Diplomacy", 0.22807133696665638]]}'}
    assert result_topics == expect
