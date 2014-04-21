from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from dota2_scrapers.items import MatchItem
from dota2.models import Hero, Player

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
        match = MatchItem()
        match['match_id'] = match_info.xpath('.//td[1]/text()').extract()[0]
        match['radiant_team'] = match_info.xpath('.//td[3]//a/text()').extract()[0]
        match['dire_team'] = match_info.xpath('.//td[4]//a/text()').extract()[0]
        winner = match_info.xpath('.//td[5]/text()').extract()[0]
        if winner.lower() == 'radiant':
            match['winner'] = 0
        elif winner.lower() == 'dire':
            match['winner'] = 1
        scoreboard = sel.xpath('//table')[1].xpath('tbody//tr')
        player_field = '%s_player_%d'
        hero_field = '%s_hero_%d'
        team = 'radiant'
        num_players = len(scoreboard) / 2
        for i in range(0, len(scoreboard)):
            if i >= 5:
                team = 'dire'
            player = scoreboard[i].xpath('.//td[1]//a/text()') or scoreboard[i].xpath('.//td[3]//a/text()')
            hero = scoreboard[i].xpath('.//td[3]//img/@alt') or scoreboard[i].xpath('.//td[4]//img/@alt')
            match[player_field % (team, i % num_players)] = Player.objects.get(player=player.extract()[0])
            match[hero_field % (team, i % num_players)] = Hero.objects.get(hero=self.heroes[hero.extract()[0]])
        return match
