### How to start locally
0. You need docker and docker-compose installed and configured in order to run the app
1. rename env.example to .example
2. Run docker compose build
3. Run docker compose up
4. Run docker exec -it alphabet_converter_app bash
5. In the console run python app/seed/seed.py
6. Go to localhost 8081/docs

## What is this app
This is a FastAPI backend application for alphabet transliterations. Currently it is not fully developed. There is no client app (but it can be tested with swagger), and no way of adding alphabets, writing systems, characters etc. This services will be added in the future. Now there is only demo (you need to seed the db with script that uses factories) with Avestan alphabet with options to convert it to Hoffmann Latin and Simplified Polish Latin. It is also possible to transliterate Hoffmann Latin to Avestan. I hope that I will be able to develop the app so it will be possible to use the app as intended, without need to seed the db.
