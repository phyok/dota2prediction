#!/bin/bash

cd dota2_scrapers
scrapy crawl datdota_hero_mapper
scrapy crawl datdota_matches
scrapy crawl datdota_players
scrapy crawl datdota_heroes
