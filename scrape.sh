#!/bin/bash

cd dota2_scrapers
scrapy crawl datdota_heroes
scrapy crawl datdota_players
scrapy crawl datdota_matches
