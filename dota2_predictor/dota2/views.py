from django.shortcuts import render
from dota2.models import Hero, Player
import simplejson as json

# Create your views here.
def index(request):
    heroes = Hero.objects.order_by('hero').values_list('hero', flat=True)
    players = Player.objects.order_by('player').values_list('player', flat=True)
    context = {
        'heroes': json.dumps(list(heroes)),
        'players': json.dumps(list(players))
    }
    return render(request, 'dota2/index.html', context)

