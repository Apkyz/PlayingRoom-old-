from django.shortcuts import get_object_or_404, redirect, render
from django import template
from django.contrib.auth.decorators import permission_required, login_required
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect

from .models import Deck, Player, Tournament, Participant, Match
from .forms import PlayerForm
from django.contrib.auth.models import User
# Create your views here.

@login_required(login_url="/login/")
def index(request):
    template = loader.get_template('player/index.html')
    players = list(Player.objects.all())
    context = {}
    context['segment'] = 'player_index'
    context['players'] = players
    return HttpResponse(template.render(context, request))

def add(request):
    template = loader.get_template('player/form.html')
    context = {}
    context['segment'] = 'player_add'
    user = get_object_or_404(User, username = request.user.username)
    form = PlayerForm(user=user)
    context['form'] = form
    if request.method == 'POST':
        player = Player()
        player.user = get_object_or_404(User, id=request.POST.get("user"))
        player.first_name = request.POST.get("first_name")
        player.last_name = request.POST.get("last_name")
        player.cosy = request.POST.get("cosy")
        player.save()
        # Créer un pop up
        return redirect(index, permanent=True)
    return HttpResponse(template.render(context, request))

def delete(request, cosy):
    player = get_object_or_404(Player, cosy = cosy)
    if player:
        player.delete()
        return redirect(index, permanent=True)
    
def view(request, cosy):
    player = get_object_or_404(Player, cosy = cosy)
    if player:
        template = loader.get_template('player/home.html')
        context = {}
        context['player'] = player
        
        participant = Participant.objects.get(player = player)
        decks = player.getDecks()
        matchs1 = list(Match.objects.filter(player1 = participant))
        matchs2 = list(Match.objects.filter(player2 = participant))
        match = list()
        for m in matchs1:
            match.append(m)
        for m in matchs2:
            match.append(m)
        
        result = list()
        win = 0
        draw = 0
        loose = 0
        for deck in decks:
            _win = 0
            _draw = 0
            _loose = 0
            for m in match:
                r = m.getResult(participant)
                
                if deck == m.deck1 or deck == m.deck2:
                    if r == 'win':
                        _win += 1
                        win += 1
                    elif r == 'loose':
                        _loose += 1
                        loose += 1
                    else:
                        _draw += 1
                        draw += 1
            result.append([deck, (_win, _draw, _loose)])
        context['winrate'] = result
        # GLOBAL 
        context['win'] = win
        context['loose'] = loose
        context['draw'] = draw
        context['match'] = match
        #context['tournament'] = tournament
        context['participant'] = participant
        return HttpResponse(template.render(context, request))
    
def edit(request, cosy):
    if request.method == 'POST':
        old_cosy = request.POST.get("old_cosy")
        user = get_object_or_404(User, pk = request.POST.get('user'))
        p = Player(
            user = user,
            first_name = request.POST.get("first_name"),
            last_name = request.POST.get("last_name"),
            cosy = request.POST.get("cosy")
        )
        player = Player.objects.filter(cosy=old_cosy).update(first_name = p.first_name, last_name = p.last_name, cosy = p.cosy)
        return redirect(index, permanent=True)
    else:
        player = get_object_or_404(Player, cosy = cosy)
        user = User.objects.get(username=request.user.username)
        if player:
            form = PlayerForm(player = player, user = user)
            template = loader.get_template('player/form.html')
            context = {}
            context['player'] = player
            context['form'] = form
            context['edit'] = True
        return HttpResponse(template.render(context, request))

def deck_add(request, cosy):
    player = get_object_or_404(Player, cosy = cosy)
    deck = Deck(name= request.POST.get("name"))
    deck.save()
    player.decks.add(deck)
    return redirect(edit, cosy, permanent=True)

def deck_remove(request, cosy, id):
    player = get_object_or_404(Player, cosy = cosy)
    deck = get_object_or_404(Deck, id = id)
    player.decks.remove(deck)
    return redirect(edit, cosy, permanent=True)

def match_add(request):
    if request.method == 'POST':
        match = Match(
            player1 = request.POST.get["player1"],
            deck1 = request.POST.get["deck1"],
            player2 = request.POST.get["player2"],
            deck2 = request.POST.get["deck2"],
            winner = request.POST.get["winner"]
        )
    else:
        print("else")
    return redirect(index, permanent=True)