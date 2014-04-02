from scrapy.item import Item, Field
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

class Hero(Item):
    name = Field(serializer=str)
    win_rate = Field(serializer=lambda x: float(x.replace('%', '')))
    matches_played = Field(serializer=lambda x: int(x.replace(',', '')))
    kda_ratio = Field(serializer=lambda x: float(x))

class DotabuffSpider(CrawlSpider):
    name = 'dotabuff'
    start_urls = ['http://dotabuff.com']
    rules = [Rule(SgmlLinkExtractor(allow='heroes\/winning\?date='), 'parse_hero')]

    def parse_hero(self, response):
        heroes = []
        sel = Selector(response)
        for row in sel.xpath('//table//tbody//tr'):
            hero = Hero()
            hero['name'] = row.xpath('.//td[2]//a[@class="hero-link"]/text()').extract()[0]
            hero['win_rate'] = row.xpath('.//td[3]//div[1]/text()').extract()[0]
            hero['matches_played'] = row.xpath('.//td[4]//div[1]/text()').extract()[0]
            hero['kda_ratio'] = row.xpath('.//td[5]//div[1]/text()').extract()[0]
            heroes.append(hero)
        return heroes
