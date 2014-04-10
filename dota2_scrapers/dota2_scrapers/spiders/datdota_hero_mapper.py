from scrapy.item import Item, Field
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

class Hero(Item):
    hero = Field(serializer=str)
    hero_alt = Field(serializer=str)

class DatDotaHeroMapperSpider(Spider):
    name = 'datdota_hero_mapper'
    start_urls = ['http://www.datdota.com/directory.php?q=Hero']

    def parse(self, response):
        sel = Selector(response)
        heroes = sel.xpath('//table')[0].xpath('tbody//tr')
        for hero in heroes:
            h = Hero()
            h['hero'] = hero.xpath('.//td[1]//a/text()').extract()[0]
            h['hero_alt'] = hero.xpath('.//td[2]//img/@alt').extract()[0]
            yield h
