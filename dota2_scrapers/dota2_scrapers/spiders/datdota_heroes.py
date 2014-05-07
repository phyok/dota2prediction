from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from dota2_scrapers.items import HeroItem

class DatDotaHeroesSpider(Spider):
    name = 'datdota_heroes'
    start_urls = ['http://www.datdota.com/directory.php?q=Hero',
                  'http://www.datdota.com/heroes.php']
    heroes = {}

    def parse(self, response):
        sel = Selector(response)
        if response.url == 'http://www.datdota.com/directory.php?q=Hero':
            heroes = sel.xpath('//table')[0].xpath('tbody//tr')
            for h in heroes:
                hero = h.xpath('.//td[1]//a/text()').extract()[0]
                hero_alt = h.xpath('.//td[2]//img/@alt').extract()[0]
                DatDotaHeroesSpider.heroes[hero] = hero_alt
        elif response.url == 'http://www.datdota.com/heroes.php':
            heroes = sel.xpath('//table')[0].xpath('tbody//tr')
            for hero in heroes:
                h = HeroItem()
                h['hero'] = hero.xpath('.//td[1]//a/text()').extract()[0]
                h['hero_alt'] = DatDotaHeroesSpider.heroes[h['hero']]
                h['matches'] = hero.xpath('.//td[2]/text()').extract()[0]
                h['wins'] = hero.xpath('.//td[3]/text()').extract()[0]
                h['losses'] = hero.xpath('.//td[4]/text()').extract()[0]
                h['win_rate'] = hero.xpath('.//td[5]/text()').extract()[0]
                yield h
