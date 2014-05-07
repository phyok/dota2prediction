from scrapy.contrib.djangoitem import DjangoItem
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from dota2_scrapers.items import PlayerItem

class DatDotaPlayersSpider(Spider):
    name = 'datdota_players'
    start_urls = ['http://www.datdota.com/players.php']

    def parse(self, response):
        sel = Selector(response)
        players = sel.xpath('//table')[0].xpath('tbody//tr')
        for player in players:
            p = PlayerItem()
            p['player'] = player.xpath('.//td[1]//a/text()').extract()[0]
            p['matches'] = player.xpath('.//td[2]/text()').extract()[0]
            p['wins'] = player.xpath('.//td[3]/text()').extract()[0]
            p['losses'] = player.xpath('.//td[4]/text()').extract()[0]
            p['win_rate'] = player.xpath('.//td[5]/text()').extract()[0]
            yield p
