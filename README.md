# Hermes

## Running

Hermes requires docker-compose, which you can install via `sudo pip install -U
docker-compose`. If you're on OS X be sure to set your environemnt variable
correctly using: `(boot2docker shellinit)`.

Then its as simple as `docker-compose up`. To test if the api is working you can use cURL:

```bash
curl -i -u user:text2features -H "Content-Type: application/json" -d
'{"content": "A Labour councillor’s son who was detained in Turkey on suspicion
of trying to enter Syria illegally is being flown back to the UK, it has been
claimed."}' -X POST http://localhost:5000/
```

If you are on OS X, swap out `localhost` for whatever your boot2docker IP
address is. You can find this by running `boot2docker ip`.
