from django.db import models

class Hero(models.Model):
    hero = models.CharField(max_length=100, unique=True)
    matches = models.PositiveIntegerField()
    wins = models.PositiveIntegerField()
    losses = models.PositiveIntegerField()
    win_rate = models.FloatField()
    hero_alt = models.CharField(max_length=100)

    def __str__(self):
        return self.hero

class Player(models.Model):
    player = models.CharField(max_length=100, unique=True)
    matches = models.PositiveIntegerField()
    wins = models.PositiveIntegerField()
    losses = models.PositiveIntegerField()
    win_rate = models.FloatField()

    def __str__(self):
        return self.player

class Match(models.Model):
    match_id = models.PositiveIntegerField(primary_key=True)
    radiant_team = models.CharField(max_length=100)
    dire_team = models.CharField(max_length=100)
    winner = models.SmallIntegerField()
    radiant_player_0 = models.ForeignKey(Player, related_name='+', blank=True, null=True)
    radiant_player_1 = models.ForeignKey(Player, related_name='+', blank=True, null=True)
    radiant_player_2 = models.ForeignKey(Player, related_name='+', blank=True, null=True)
    radiant_player_3 = models.ForeignKey(Player, related_name='+', blank=True, null=True)
    radiant_player_4 = models.ForeignKey(Player, related_name='+', blank=True, null=True)
    radiant_hero_0 = models.ForeignKey(Hero, related_name='+')
    radiant_hero_1 = models.ForeignKey(Hero, related_name='+')
    radiant_hero_2 = models.ForeignKey(Hero, related_name='+')
    radiant_hero_3 = models.ForeignKey(Hero, related_name='+')
    radiant_hero_4 = models.ForeignKey(Hero, related_name='+')
    dire_player_0 = models.ForeignKey(Player, related_name='+', blank=True, null=True)
    dire_player_1 = models.ForeignKey(Player, related_name='+', blank=True, null=True)
    dire_player_2 = models.ForeignKey(Player, related_name='+', blank=True, null=True)
    dire_player_3 = models.ForeignKey(Player, related_name='+', blank=True, null=True)
    dire_player_4 = models.ForeignKey(Player, related_name='+', blank=True, null=True)
    dire_hero_0 = models.ForeignKey(Hero, related_name='+')
    dire_hero_1 = models.ForeignKey(Hero, related_name='+')
    dire_hero_2 = models.ForeignKey(Hero, related_name='+')
    dire_hero_3 = models.ForeignKey(Hero, related_name='+')
    dire_hero_4 = models.ForeignKey(Hero, related_name='+')

    def __str__(self):
        return str(self.match_id)
