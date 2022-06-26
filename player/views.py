from django.shortcuts import redirect, render
from django import template
from django.contrib.auth.decorators import permission_required, login_required
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import redirect

from .models import Deck, Player, Championship

# Create your views here.

@login_required(login_url="/login/")
def index(request):
    template = loader.get_template('player/index.html')
    players = Player.objects.all()
    context = { 
        'segment': 'player_index',
        'players': players,
    }
    return HttpResponse(template.render(context, request))

def add(request):
    template = loader.get_template('player/index.html')
    context = { 
        'segment': 'player_index',
    }
    # deck1 = Deck(name = 'Sky Striker')
    # deck2 = Deck(name = 'Dragon Link')
    # deck1.save()
    # deck2.save()
    
    # player1 = Player(first_name = 'Nicola', last_name = 'La Mattina', cosy = '03123456789')
    # player2 = Player(first_name = 'Alexandre', last_name = 'Appez', cosy = '0123456789')
    # player1.save()
    # player2.save()
    
    # player1.decks.add(deck1)
    # player2.decks.add(deck2)
    
    Deck.objects.filter(name='Sky Striker').update(name='Evil Twin')
    # players = list()
    # player1 = Player(first_name = 'Nicola', last_name = 'La Mattina', cosy = '03123456789')
    # player2 = Player(first_name = 'Alexandre', last_name = 'Appez', cosy = '0123456789')
    # player1.save()
    # player2.save()
    # players.append(Player(first_name = 'Charles', last_name = 'Thomas', cosy = '012365498981'))
    # players.append(Player(first_name = 'Quentin', last_name = 'Sente', cosy = '036519841'))
    # players.append(Player(first_name = 'Maxime', last_name = 'Martin', cosy = '9984980816'))
    # players.append(Player(first_name = 'Loris', last_name = 'Hubin', cosy = '65190840'))
    # players.append(Player(first_name = 'Dimitri', last_name = 'Popadinec', cosy = '984098749510'))
    # players.append(Player(first_name = 'Corentin', last_name = 'Letelier', cosy = '649840984'))
    # for i in players:
    #     i.save()
    
    return redirect(index)
    