from django.shortcuts import render
from django.http import HttpResponse
from dota2.models import Hero, Player
from django import forms
import simplejson as json
import random

class PredictionForm(forms.Form):
    dire_player_0 = forms.CharField()
    dire_hero_0 = forms.CharField()
    dire_player_1 = forms.CharField()
    dire_hero_1 = forms.CharField()
    dire_player_2 = forms.CharField()
    dire_hero_2 = forms.CharField()
    dire_player_3 = forms.CharField()
    dire_hero_3 = forms.CharField()
    dire_player_4 = forms.CharField()
    dire_hero_4 = forms.CharField()
    radiant_player_0 = forms.CharField()
    radiant_hero_0 = forms.CharField()
    radiant_player_1 = forms.CharField()
    radiant_hero_1 = forms.CharField()
    radiant_player_2 = forms.CharField()
    radiant_hero_2 = forms.CharField()
    radiant_player_3 = forms.CharField()
    radiant_hero_3 = forms.CharField()
    radiant_player_4 = forms.CharField()
    radiant_hero_4 = forms.CharField()

# Create your views here.
def index(request):
    heroes = Hero.objects.order_by('hero').values_list('hero', flat=True)
    players = Player.objects.order_by('player').values_list('player', flat=True)
    context = {
        'heroes': json.dumps(list(heroes)),
        'players': json.dumps(list(players))
    }
    return render(request, 'dota2/index.html', context)

def prediction(request):
    if request.method == 'GET':
        form = PredictionForm(request.GET)
        context = dict(form.data)
        for key, value in context.items():
            context[key] = value[0]
        context['prediction'] = predict(form.data)
        return render(request, 'dota2/prediction.html', context)
 
def predict(data):
    winner = random.randint(0, 1);
    prediction = None;
    if winner == 0:
        prediction = 'radiant victory!'
    else:
        prediction = 'dire victory!'
    return prediction
