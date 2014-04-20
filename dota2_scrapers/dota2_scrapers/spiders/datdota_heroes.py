from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from dota2_scrapers.items import HeroItem

class DatDotaPlayersSpider(Spider):
    name = 'datdota_heroes'
    start_urls = ['http://www.datdota.com/heroes.php']

    def parse(self, response):
        sel = Selector(response)
        heroes = sel.xpath('//table')[0].xpath('tbody//tr')
        for hero in heroes:
            h = HeroItem()
            h['hero'] = hero.xpath('.//td[1]//a/text()').extract()[0]
            h['matches'] = hero.xpath('.//td[2]/text()').extract()[0]
            h['wins'] = hero.xpath('.//td[3]/text()').extract()[0]
            h['losses'] = hero.xpath('.//td[4]/text()').extract()[0]
            h['win_rate'] = hero.xpath('.//td[5]/text()').extract()[0]
            yield h
