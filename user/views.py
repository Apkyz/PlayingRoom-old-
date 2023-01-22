from django.shortcuts import render
from django import template
from django.contrib.auth.decorators import permission_required, login_required
from django.template import loader
from django.http import HttpResponse
from player.models import Player
from django.contrib.auth.models import User
# Create your views here.

@login_required(login_url="/login/")
def index(request):
    template = loader.get_template('user/index.html')
    context = {}
    user = User.objects.get(username=request.user.username)
    try:
        context['player'] = Player.objects.get(user = user)
    except:
        print('[ERROR] : Pas de player')
    context['segment'] = 'user_index'
    return HttpResponse(template.render(context, request))

def edit(request):
    template = loader.get_template('user/index.html')
    context = {}
    context['segment'] = 'user_index'
    return HttpResponse(template.render(context, request))