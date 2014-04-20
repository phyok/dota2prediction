# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.contrib.djangoitem import DjangoItem
from dota2.models import Hero, Player, Match

class Dota2ScrapersItem(DjangoItem):

    def update(self):
        pass

class HeroItem(Dota2ScrapersItem):
    django_model = Hero

    def update(self):
        hero = self.save(commit=False)
        hero_set = Hero.objects.filter(hero=hero.hero)
        if len(hero_set) == 0:
            self.save()
        else:
            hero_set.update(matches=hero.matches,
                            wins=hero.wins,
                            losses=hero.losses,
                            win_rate=hero.win_rate)

class PlayerItem(Dota2ScrapersItem):
    django_model = Player

    def update(self):
        player = self.save(commit=False)
        player_set = Player.objects.filter(player=player.player)
        if len(player_set) == 0:
            self.save()
        else:
            player_set.update(matches=player.matches,
                              wins=player.wins,
                              losses=player.losses,
                              win_rate=player.win_rate)

def serialize_winner(side):
    if side.lower() == 'radiant':
        return 0
    elif side.lower() == 'dire':
        return 1
    else:
        return None

class MatchItem(Dota2ScrapersItem):
    django_model = Match
    
    def update(self):
        self.save()
