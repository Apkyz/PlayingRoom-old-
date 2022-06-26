from django.shortcuts import render
from django import template
from django.contrib.auth.decorators import permission_required, login_required
from django.template import loader
from django.http import HttpResponse

# Create your views here.

@login_required(login_url="/login/")
def index(request):
    template = loader.get_template('user/index.html')
    context = { 
        'segment': 'user_index',
    }
    return HttpResponse(template.render(context, request))
