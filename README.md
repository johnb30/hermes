# Hermes

## Services

Hermes serves as a RESTful API wrapper for a number of text processing
services, allowing for the quick generation of text features. We've tried to
make it as easy as possible to deploy the service on your own system by
containerizing each piece with [Docker](https://www.docker.com/whatisdocker/) (i.e. text
features in a box). The following services are currently implemented:

- **MITIE:** [MIT Infromation Extraction](https://github.com/mit-nlp/MITIE)
- **CLIFF:** [Server](https://github.com/c4fcm/CLIFF) for
    [CLAVIN](https://github.com/Berico-Technologies/CLAVIN/tree/stable/1.1.x).
    Andy Halterman has an image for running CLIFF over on [Docker
    Hub](https://registry.hub.docker.com/u/ahalterman/cliff/)
- **Topic Models:** LDA model with 50 topics, impleneted in
    [gensim](https://radimrehurek.com/gensim/)

## Running

Hermes requires docker-compose, which you can install via `sudo pip install -U
docker-compose`. If you're on OS X be sure to set your environment variable
correctly using: `(boot2docker shellinit)`.

Then its as simple as `docker-compose up`. To test if the api is working you can use cURL:

```bash
curl -i -u user:text2features -H "Content-Type: application/json" -d
'{"content": "Insurgents bombarded a government-held part of Syria'"'"'s second
city Aleppo overnight, killing at least eight people, Syrian state media
reported. The Syrian Observatory for Human Rights, a UK-based group that tracks the war,
said eight people were killed in an air strike by government forces in a
separate, rebel-held part of the city."}' -X POST http://localhost:5000/
```

If you are on OS X, swap out `localhost` for whatever your boot2docker IP
address is. You can find this by running `boot2docker ip`.

The response should look like this:

```http
HTTP/1.1 201 CREATED
Content-Type: application/json
Content-Length: 3238
Server: TornadoServer/4.1

{"MITIE": {"entities": "[{\"start\": 6, \"entity_text\": \"Syria\", \"tag\":
\"LOCATION\", \"stop\": 7, \"score\": 1.1885840007455295}, {\"start\": 10,
\"entity_text\": \"Aleppo\", \"tag\": \"LOCATION\", \"stop\": 11, \"score\":
0.6466367651771303}, {\"start\": 19, \"entity_text\": \"Syrian\", \"tag\":
\"MISC\", \"stop\": 20, \"score\": 1.1922037730890405}, {\"start\": 28,
\"entity_text\": \"Human Rights\", \"tag\": \"ORGANIZATION\", \"stop\": 30,
\"score\": 0.6246598122395554}, {\"start\": 32, \"entity_text\": \"UK-based\",
\"tag\": \"MISC\", \"stop\": 33, \"score\": 1.3681621776612611}]", "html":
"\"Insurgents bombarded a government-held part of Syria 's second city Aleppo
overnight , killing at least eight people , Syrian state media reported . The
Syrian Observatory for <span class=\\\"mitie-ORGANIZATION\\\">Human
Rights</span> , a UK-based group that tracks the war , said eight people were
killed in an air strike by government forces in a separate , rebel-held part of
the city .\"", "cleaned_tokens": "[\"insurgents\", \"bombarded\",
\"governmentheld\", \"part\", \"syria\", \"second\", \"city\", \"aleppo\",
\"overnight\", \"killing\", \"least\", \"eight\", \"people\", \"syrian\",
\"state\", \"media\", \"reported\", \"syrian\", \"observatory\", \"human\",
\"rights\", \"ukbased\", \"group\", \"tracks\", \"war\", \"said\", \"eight\",
\"people\", \"were\", \"killed\", \"air\", \"strike\", \"government\",
\"forces\", \"separate\", \"rebelheld\", \"part\", \"city\"]"}, "topics":
"{\"topics\": [[3, 0.034244257290796241], [13, 0.46896935908923226], [16,
0.19981398092786712], [37, 0.17114902515097302], [38, 0.10213916701481499]],
\"highest_topic_string\": \"Control\", \"highest_topic_index\": 13,
\"topic_strings\": [[\"Assad\", 0.034244257290796241], [\"Control\",
0.46896935908923226], [\"Cities\", 0.19981398092786712], [\"Rebels\",
0.17114902515097302], [\"Kobani\", 0.10213916701481499]]}", "CLIFF": {"status":
"ok", "version": "2.0.0", "results": {"organizations": [{"count": 1, "name":
"Syrian Observatory for Human Rights"}], "places": {"mentions": [{"confidence":
1.0, "name": "Syrian Arab Republic", "countryCode": "SY", "featureCode":
"PCLI", "lon": 38.0, "source": {"charIndex": 47, "string": "Syria"},
"stateCode": "00", "featureClass": "A", "lat": 35.0, "id": 163843,
"population": 22198110}, {"confidence": 1.0, "name": "Aleppo", "countryCode":
"SY", "featureCode": "PPLA", "lon": 37.16117, "source": {"charIndex": 67,
"string": "Aleppo"}, "stateCode": "09", "featureClass": "P", "lat": 36.20124,
"id": 170063, "population": 1602264}], "focus": {"states": [{"name": "Aleppo
Governorate", "countryCode": "SY", "featureCode": "ADM1", "lon": 37.61667,
"score": 1, "stateCode": "09", "featureClass": "A", "lat": 36.25, "id": 170062,
"population": 3115559}], "cities": [{"name": "Aleppo", "countryCode": "SY",
"featureCode": "PPLA", "lon": 37.16117, "score": 1, "stateCode": "09",
"featureClass": "P", "lat": 36.20124, "id": 170063, "population": 1602264}],
"countries": [{"name": "Syrian Arab Republic", "countryCode": "SY",
"featureCode": "PCLI", "lon": 38.0, "score": 2, "stateCode": "00",
"featureClass": "A", "lat": 35.0, "id": 163843, "population": 22198110}]}},
"people": []}, "milliseconds": 55}}%
```
