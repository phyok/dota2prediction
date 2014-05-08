#!/bin/bash

cd dota2_predictor
python manage.py sqlclear dota2 | python manage.py dbshell
python manage.py syncdb
cd ..

cd dota2_scrapers
scrapy crawl datdota_heroes
scrapy crawl datdota_players
scrapy crawl datdota_matches
cd ..

cd dota2_predictor/dota2
python preprocess.py
cd ../..
