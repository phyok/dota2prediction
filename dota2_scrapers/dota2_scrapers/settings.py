# Scrapy settings for dota2_scrapers project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import sys
sys.path.append('../dota2_predictor')

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'dota2_predictor.settings'

BOT_NAME = 'dota2_scrapers'

SPIDER_MODULES = ['dota2_scrapers.spiders']
NEWSPIDER_MODULE = 'dota2_scrapers.spiders'

ITEM_PIPELINES = {
     'dota2_scrapers.pipelines.DatDotaCsvItemPipeline': 100
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'dota2_scrapers (+http://www.yourdomain.com)'
