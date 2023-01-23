from django.contrib import admin
from .models import Match, Participant, Tournament

admin.site.register(Tournament)
admin.site.register(Participant)
admin.site.register(Match)