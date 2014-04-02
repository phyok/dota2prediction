from scrapy.item import Item, Field
from scrapy.spider import Spider
from scrapy.selector import Selector
import re

class Hero(Item):
    name = Field(serializer=str)
    win_rate = Field(serializer=lambda x: float(x.replace('%', '')))
    matches_played = Field(serializer=lambda x: int(x.replace(',', '')))
    kda_ratio = Field(serializer=lambda x: float(x))

class Player(Item):
    player = Field(serializer=str)
    matches_played = Field(serializer=lambda x: int(x.replace(',', '')))
    win_rate = Field(serializer=lambda x: float(x.replace('%', '')))

class DotabuffSpider(Spider):
    name = 'dotabuff'
    start_urls = [
        'http://dotabuff.com/heroes/winning?date=',
        'http://dotabuff.com/players/verified'
        ]
    
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

    def parse_player(self, response):
        players = []
        sel = Selector(response)
        for row in sel.xpath('//table//tbody//tr'):
            player = Player()
            player['player'] = row.xpath('.//td[2]//a/text()').extract()[0]
            player['matches_played'] = row.xpath('.//td[3]//div[1]/text()').extract()[0]
            player['win_rate'] = row.xpath('.//td[4]//div[1]/text()').extract()[0]
            players.append(player)
        return players

    def parse(self, response):
        if re.search('heroes\/winning', response.url):
            return self.parse_hero(response)
        elif re.search('players\/verified', response.url):
            return self.parse_player(response)
