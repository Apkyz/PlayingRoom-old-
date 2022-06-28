from django.shortcuts import get_object_or_404, redirect, render
from django import template
from django.contrib.auth.decorators import permission_required, login_required
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect

from .models import Deck, Player, Championship
from .forms import PlayerForm
from django.forms import ModelForm
# Create your views here.

@login_required(login_url="/login/")
def index(request):
    template = loader.get_template('player/index.html')
    players = Player.objects.all()
    context = {}
    context['segment'] = 'player_index'
    context['players'] = players
    return HttpResponse(template.render(context, request))

def add(request):
    template = loader.get_template('player/form.html')
    context = {}
    context['segment'] = 'player_add'
    form = PlayerForm()
    context['form'] = form
    if request.method == 'POST':
        player = Player()
        player.first_name = request.POST.get("first_name")
        player.last_name = request.POST.get("last_name")
        player.cosy = request.POST.get("cosy")
        player.save()
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
        return HttpResponse(template.render(context, request))
    
def edit(request, cosy):
    if request.method == 'POST':
        old_cosy = request.POST.get("old_cosy")
        p = Player(
            first_name = request.POST.get("first_name"),
            last_name = request.POST.get("last_name"),
            cosy = request.POST.get("cosy")
        )
        player = Player.objects.filter(cosy=old_cosy).update(first_name = p.first_name, last_name = p.last_name, cosy = p.cosy)
        return redirect(index, permanent=True)
    else:
        player = get_object_or_404(Player, cosy = cosy)
        if player:
            form = PlayerForm(player=player)
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