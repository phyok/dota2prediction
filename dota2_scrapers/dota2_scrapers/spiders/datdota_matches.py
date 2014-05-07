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
        # Page layout is inconsistent.  Sometimes, Radiant and Dire are
        # in the same table.  Other times, they have separate tables.
        scoreboard = sel.xpath('//table')[1].xpath('tbody//tr')
        radiant_scoreboard = None
        dire_scoreboard = None
        if len(scoreboard) == 10:
            radiant_scoreboard = scoreboard[:5]
            dire_scoreboard = scoreboard[5:]
        else:
            radiant_scoreboard = scoreboard
            dire_scoreboard = sel.xpath('//table')[2].xpath('tbody//tr')
        player_field = '%s_player_%d'
        hero_field = '%s_hero_%d'
        num_players = 10
        team = 'radiant'
        scoreboard = radiant_scoreboard
        for i in range(0, num_players):
            j = i % 5
            if i >= 5:
                team = 'dire'
                scoreboard = dire_scoreboard
            player = scoreboard[j].xpath('.//td[1]//a/text()') or scoreboard[j].xpath('.//td[3]//a/text()')
            hero = scoreboard[j].xpath('.//td[3]//img/@alt') or scoreboard[j].xpath('.//td[4]//img/@alt')
            try:
                match[player_field % (team, j)] = Player.objects.get(player=player.extract()[0])
            except Exception:
                pass
            match[hero_field % (team, j)] = Hero.objects.get(hero_alt=hero.extract()[0])
        return match
