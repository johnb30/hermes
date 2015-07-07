# Hermes 

[Hermes Conrad](http://futurama.wikia.com/wiki/Hermes_Conrad) is the ~~unofficial~~ official
mascot of the Hermes API.

## Services

Hermes is a RESTful API wrapper for a number of text processing
services, allowing for the quick generation of text features. We've tried to
make it as easy as possible to deploy the service on your own system by
containerizing each piece with [Docker](https://www.docker.com/whatisdocker/) (i.e. text
features in a box). The following services are currently implemented:

- **MITIE:** [MIT Infromation Extraction](https://github.com/mit-nlp/MITIE).
- **CLIFF:** [Server](https://github.com/c4fcm/CLIFF) for
    [CLAVIN](https://github.com/Berico-Technologies/CLAVIN/tree/stable/1.1.x).
    Andy Halterman has an image for running CLIFF over on [Docker
    Hub](https://registry.hub.docker.com/u/ahalterman/cliff/).
- **Topic Model:** LDA model with 50 topics, implemented in
    [gensim](https://radimrehurek.com/gensim/). Designed for a specific set of
    topics. Only stories geolocated to Iraq or Syria are run through this container.
- **Joshua:** [Machine translation](http://joshua-decoder.org/)
- **Mordecai:** Geolocation provided by
  [Mordecai](https://github.com/caerusassociates/mordecai), a full-text
  geolocation tool developed by [Caerus
  Associates](http://caerusassociates.com/).

## Fields

Hermes returns the following fields from each service:

- **MITIE**
    - `MITIE`:
        - `entities`: An array of objects containing the following members.
            - `entity_text`: String. The actual text pulled from the string (Ex: Syria).
            - `tag`: String. The MITIE tag for the entity text (Ex: LOCATION).
            - `start`: Integer. The start of the entity location in the string (Ex: 6).
            - `stop`: Integer. The end of the entity location in the string (Ex: 7).
            - `score`: Float. The MITIE confidence score (Ex: 1.1885840007455295).
        - `html`: HTML generated for highlighting entities in dashboards, etc.
- **Mordecai**
    - `Mordecai`:
        - `focus_countries`: Dictionary of countries and the number of times each was
          found in the text.
        - `country_vec`: List of countries found in the text.
        - `locations`: List of dictionaries including the lat, lon, country code,
          placename, and term used to search Geonames for each location found in
          the text.
- **CLIFF**
    - `CLIFF`:
        - `cliff_people`: List of people extracted by CLIFF's NER.
        - `cliff_orgs`: List of organizations extracted by CLIFF's NER.
        - `focus_cities`: List of dictionaries including the lat, lon, name, stateName, 
          and countryCode of the cities identified as the focus.
        - `focus_states`: List of dictionaries including the lat, lon, name, stateCode, 
          and countryCode of the states/governorates/provinces/etc. identified as the focus.
        - `focus_countries`: List of dictionaries including the lat, lon, name, and countryCode 
          of the countries identified as the focus.
        - `country_vec`: List of countryCodes.
        - `stateVec`: List of states/governorates/provinces.
- **Topic Model**
    - `topic_model`:
        - `topics`: Array of arrays that contains the topic index as the first
          entry in the inner arrays and the topic weighting as the second
          entry.
        - `highest_topic_string`: String representation of the topic with the
          highest weighting for that document.
        - `highest_topic_index`: Integer representation of the topic with the
          highest weighting for that document.
        - `topic_strings`: Array of arrays that contains the string
          representation of the topic as the first entry in the inner arrays
          and the topic weighting as the second entry.
- **Joshua**
    - `translated_content`: English translation of Arabic text.


## Running

Make sure you have docker installed first. You can get everything setup using
the `standup.sh` script in this repo, or do it yourself. Instructions for Ubuntu can be found
[here](http://docs.docker.com/installation/ubuntulinux/) and for OS X (via
boot2docker) [here](https://docs.docker.com/installation/mac/). Hermes requires
docker-compose, which you can install via `sudo pip install -U docker-compose`.
If you're on OS X be sure to set your environment variable correctly using:
`(boot2docker shellinit)`.

Then its as simple as `sudo docker-compose up`. You can pass it the `-d` flag
to run the process in the background. If you want to kill the containers just issue
`sudo docker-compose kill`. 

There is a main endpoint `/hermes` and four service specific endpoints.
`/hermes/mitie`, `/hermes/mordecai`, `/hermes/cliff`, and `/hermes/topics`.

To test if the api is working you can use cURL:

```bash
curl -i -u user:text2features -H "Content-Type: application/json" -d '{"content": "Insurgents bombarded a government-held part of Syria'"'"'s second city Aleppo overnight, killing at least eight people, Syrian state media reported. The Syrian Observatory for Human Rights, a UK-based group that tracks the war, said eight people were killed in an air strike by government forces in a separate, rebel-held part of the city."}' -X POST http://localhost:5000/hermes
```

To run using the Python `requests` library:

```python
import json
import requests

headers = {'Content-Type': 'application/json'}
# Specification of the lang argument is optional.
data = {"content": "Insurgents bombarded a government-held part of Syria's second city Aleppo overnight, killing at least eight people, Syrian state media reported. The Syrian Observatory for Human Rights, a UK-based group that tracks the war, said eight people were killed in an air strike by government forces in a separate, rebel-held part of the city.", "lang": "en"}
data = json.dumps(data)
out = requests.post('http://localhost:5000/hermes', data=data, auth=('user', 'text2features'), headers=headers)
```

If you are on OS X, swap out `localhost` for whatever your boot2docker IP
address is. You can find it by running `boot2docker ip`.

The response should look like this:

```http
HTTP/1.1 201 CREATED
Content-Type: application/json
Content-Length: 15823
Server: TornadoServer/4.1

{
    "mordecai": {
        "focus_countries": {"SYR": 1},
        "country_vec": ["SYR"],
        "locations": [{"lat": 36.20124, "searchterm": "Aleppo", "lon": 37.16117, "countrycode": "SYR", "placename": "Aleppo"}]},
    "MITIE": {
        "entities": [
        {"start": 6, "entity_text": "Syria", "tag": "LOCATION", "stop": 7, "score": 1.1885840007455295}, {"start": 10, "entity_text": "Aleppo", "tag": "LOCATION", "stop": 11, "score": 0.6466367651771303},
        {"start": 19, "entity_text": "Syrian", "tag": "MISC", "stop": 20, "score": 1.1922037730890405}, {"start": 28, "entity_text": "Human Rights", "tag": "ORGANIZATION", "stop": 30, "score": 0.6246598122395554},
        {"start": 32, "entity_text": "UK-based", "tag": "MISC", "stop": 33, "score": 1.3681621776612611}
        ],
        "html": ""Insurgents bombarded a government-held part of Syria's second city Aleppo overnight , killing at least eight people , Syrian state media reported . The Syrian Observatory for <span class="mitie-ORGANIZATION">Human Rights</span> , a UK-based group that tracks the war , said eight people were killed in an air strike by government forces in a separate , rebel-held part of the city .""},
    "stanford": "",
    "topic_model": {
        "topics": [[3, 0.034243498707272987], [13, 0.46906614953072645], [16, 0.19962228098935678], [37, 0.17123127281259765], [38, 0.10215258743372989]],
        "highest_topic_string": "Control",
        "highest_topic_index": 13,
        "topic_strings": [["Assad", 0.034243498707272987], ["Control", 0.46906614953072645], ["Cities", 0.19962228098935678], ["Rebels", 0.17123127281259765], ["Kobani", 0.10215258743372989]]
    },
    "CLIFF": {
        "focus_countries": [{"lat": 35.0, "lon": 38.0, "name": "Syrian Arab Republic", "countryCode": "SYR"}],
        "cliff_orgs": ["Syrian Observatory for Human Rights"],
        "focus_cities": [{"lat": 36.20124, "stateName": "Aleppo Governorate", "lon": 37.16117, "name": "Aleppo", "countryCode": "SYR"}],
        "country_vec": ["SYR"],
        "cliff_people": [],
        "focus_states": [{"lat": 36.25, "lon": 37.61667, "name": "Aleppo Governorate", "countryCode": "SYR", "stateCode": "09"}],
        "stateVec": ["Aleppo Governorate"]
    }
}

```
