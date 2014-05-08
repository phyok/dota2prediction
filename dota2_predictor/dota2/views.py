from django.shortcuts import render
from django.http import HttpResponse
from dota2.models import Hero, Player
from django import forms
import simplejson as json
import random
import numpy as np
from sklearn import linear_model
import csv

# load training data
f = open('trainingdata.npz')
dat = np.load(f)
X = dat['X']
y = dat['y']
f.close()

logistic_reg = linear_model.LogisticRegression()
logistic_model = logistic_reg.fit(X, y)

heromap = {}
for key, val in csv.reader(open("hero_map.csv")):
    heromap[key] = val

playermap = {}
for key, val in csv.reader(open("player_map.csv")):
    playermap[key] = val

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

def process_data(data):
    FEATURE_SET_SIZE = 5898
    DIRE_OFFSET = 2949

    query = np.zeros((1,FEATURE_SET_SIZE))
    radiant_heros = []
    dire_heros = []
    radiant_players = []
    dire_players = []

    radiant_heros.append(str(data[u'radiant_hero_0']))
    radiant_heros.append(str(data[u'radiant_hero_1']))
    radiant_heros.append(str(data[u'radiant_hero_2']))
    radiant_heros.append(str(data[u'radiant_hero_3']))
    radiant_heros.append(str(data[u'radiant_hero_4']))

    dire_heros.append(str(data[u'dire_hero_0']))
    dire_heros.append(str(data[u'dire_hero_1']))
    dire_heros.append(str(data[u'dire_hero_2']))
    dire_heros.append(str(data[u'dire_hero_3']))
    dire_heros.append(str(data[u'dire_hero_4']))

    radiant_players.append(str(data[u'radiant_player_0']))
    radiant_players.append(str(data[u'radiant_player_1']))
    radiant_players.append(str(data[u'radiant_player_2']))
    radiant_players.append(str(data[u'radiant_player_3']))
    radiant_players.append(str(data[u'radiant_player_4']))

    dire_players.append(str(data[u'dire_player_0']))
    dire_players.append(str(data[u'dire_player_1']))
    dire_players.append(str(data[u'dire_player_2']))
    dire_players.append(str(data[u'dire_player_3']))
    dire_players.append(str(data[u'dire_player_4']))
    for i in range(5):
        query[0,int(heromap[radiant_heros[i]])] = 1
        query[0,(int(heromap[dire_heros[i]])+DIRE_OFFSET)] = 1
        query[0,int(playermap[radiant_players[i]])] = 1
        query[0,(int(playermap[dire_players[i]])+DIRE_OFFSET)] = 1
    return query

def predict(data):
    q = process_data(data)
    print logistic_model.predict_proba(q)
    winner = logistic_model.predict(q)#random.randint(0, 1);
    prediction = None;
    if winner == 0:
        prediction = 'radiant victory!'
    else:
        prediction = 'dire victory!'
    return prediction
