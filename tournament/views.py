from django.shortcuts import get_object_or_404, redirect, render
from django import template
from django.contrib.auth.decorators import permission_required, login_required
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect

from player.models import Participant, Player, Tournament, Match
from .forms import MatchForm, TournamentForm
# Create your views here.
@login_required(login_url="/login/")
def index(request):
    template = loader.get_template('tournament/index.html')
    context = {}
    tournaments = list(Tournament.objects.all())
    context['tournaments'] = tournaments
    context['segment'] = 'tournament_index'
    return HttpResponse(template.render(context, request))

def add(request):
    template = loader.get_template('tournament/form.html')
    context = {}
    context['segment'] = 'tournament_add'
    form = TournamentForm()
    context['form'] = form
    if request.method == 'POST':
        tournament = Tournament(
            name = request.POST.get("name"),
            date = request.POST.get("date"),
            id_challonge = request.POST.get("id_challonge")
        )
        tournament.save()
        return redirect(index, permanent=True)
    return HttpResponse(template.render(context, request))

def view(request, id):
    template = loader.get_template('tournament/view.html')
    context = {}
    tournament = Tournament.objects.get(pk = id)
    context['tournament'] = tournament
    return HttpResponse(template.render(context, request))

def view_participant(request, id, participant):
    template = loader.get_template('tournament/participant/view.html')
    context = {}
    tournament = Tournament.objects.get(pk = id)
    participant = Participant.objects.get(pk = participant)
    context['tournament'] = tournament
    context['participant'] = participant
    return HttpResponse(template.render(context, request))
    
def participant_add(request, id):
    template = loader.get_template('tournament/participant/add.html')
    context = {}
    tournament = Tournament.objects.get(pk = id)
    context['tournament'] = tournament
    players = list(Player.objects.all())
    participant = list(tournament.participants.all())
    lst = []
    for i in players:
        lst.append(i)
        for j in participant:
            if j.player == i:
                lst.pop(lst.index(i))
                break
    context['players'] = lst
    if request.method == 'POST':
        result = request.POST.dict()
        result.pop('csrfmiddlewaretoken')
        result.pop('table_id_length')
        for i in result:
            player = Player.objects.get(pk = int(result[i]))
            participant = Participant(payed = False)
            participant.player = player
            participant.save()
            tournament.participants.add(participant)
        return redirect(view, id, permanent = True)
    return HttpResponse(template.render(context, request))

def participant_update(request, id_t, id):
    participant = get_object_or_404(Participant, pk=id)
    if participant:
        if participant.payed:
            participant.payed = False
        else:
            participant.payed = True
        participant.save()
    return redirect(view, id_t, permanent=True)

def participant_edit(request, id_t, id):
    context = {}
    if request.method == 'POST':
        participant = id
        return redirect(view, id_t, permanent=True)
    else:
        participant = get_object_or_404(Participant, pk=id)
        if participant:
            context['participant'] = participant
        else:
            raise
    return HttpResponse(template.render(context, request))
    

def tournament_matchs_add(request, id, id_p1, id_p2):
    template = loader.get_template('tournament/match/add.html')
    context = {}
    tournament = get_object_or_404(Tournament, pk=id)
    if request.method == 'POST':
        match = Match(
            player1 = request.POST.get("player1"),
            deck1 = request.POST.get("deck1"),
            player2 = request.POST.get("player2"),
            deck2 = request.POST.get("deck2"),
            winner = request.POST.get("winner")
        )
        match.save()
        return redirect(view, id)
    else:
        p1 = Participant.objects.get(pk = id_p1)
        p2 = Participant.objects.get(pk = id_p2)
        context['player1'] = p1
        context['player2'] = p2
        context['form'] = MatchForm(tournament, p1, p2)
        context['tournament'] = tournament
    return HttpResponse(template.render(context, request))
