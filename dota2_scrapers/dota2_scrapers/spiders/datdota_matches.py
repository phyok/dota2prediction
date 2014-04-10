from scrapy.item import Item, Field
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

class Match(Item):
   match_id = Field(serializer=int)
   radiant_team = Field(serializer=str)
   dire_team = Field(serializer=str)
   winner = Field(serializer=str)
   radiant_player_0 = Field(serializer=str)
   radiant_player_1 = Field(serializer=str)
   radiant_player_2 = Field(serializer=str)
   radiant_player_3 = Field(serializer=str)
   radiant_player_4 = Field(serializer=str)
   radiant_hero_0 = Field(serializer=str)
   radiant_hero_1 = Field(serializer=str)
   radiant_hero_2 = Field(serializer=str)
   radiant_hero_3 = Field(serializer=str)
   radiant_hero_4 = Field(serializer=str)
   dire_player_0 = Field(serializer=str)
   dire_player_1 = Field(serializer=str)
   dire_player_2 = Field(serializer=str)
   dire_player_3 = Field(serializer=str)
   dire_player_4 = Field(serializer=str)
   dire_hero_0 = Field(serializer=str)
   dire_hero_1 = Field(serializer=str)
   dire_hero_2 = Field(serializer=str)
   dire_hero_3 = Field(serializer=str)
   dire_hero_4 = Field(serializer=str)

class DatDotaMatchesSpider(CrawlSpider):
    name = 'datdota_matches'
    start_urls = ['http://www.datdota.com/matches.php']
    rules = [
        Rule(SgmlLinkExtractor(allow=('match\.php\?q=\d+')), callback='parse_match'),
        Rule(SgmlLinkExtractor(allow=('matches\.php\?l0=\d+')), callback='get_more_matches', follow=True)
        ]

    def __init__(self, category=None, *args, **kwargs):
        self.heroes = {}
        super(DatDotaMatchesSpider, self).__init__(*args, **kwargs)
        hero_map = open('datdota_hero_mapper.csv', 'r')
        hero_map.readline()
        for line in hero_map:
            hero = line.strip().split(',')
            self.heroes[hero[0]] = hero[1]

    def get_more_matches(self, response):
        sel = Selector(response)
        if not sel.xpath('//table//tbody//tr'):
            raise CloseSpider('No more matches')
    
    def parse_match(self, response):
        sel = Selector(response)
        match_info = sel.xpath('//table')[0].xpath('tbody//tr')
        match = Match()
        match['match_id'] = match_info.xpath('.//td[1]/text()').extract()[0]
        match['radiant_team'] = match_info.xpath('.//td[3]//a/text()').extract()[0]
        match['dire_team'] = match_info.xpath('.//td[4]//a/text()').extract()[0]
        match['winner'] = match_info.xpath('.//td[5]/text()').extract()[0]

        scoreboard = sel.xpath('//table')[1].xpath('tbody//tr')
        player_field = '%s_player_%d'
        hero_field = '%s_hero_%d'
        team = 'radiant'
        num_players = len(scoreboard) / 2
        for i in range(0, len(scoreboard)):
            if i >= 5:
                team = 'dire'
            match[player_field % (team, i % num_players)] = scoreboard[i].xpath('.//td[3]//a/text()').extract()[0]
            match[hero_field % (team, i % num_players)] = self.heroes[scoreboard[i].xpath('.//td[4]//img/@alt').extract()[0]]
        return match
