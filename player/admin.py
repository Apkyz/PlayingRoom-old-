import imp
from django.contrib import admin
from .models import Player, Deck
# Register your models here.

admin.site.register(Player)
admin.site.register(Deck)