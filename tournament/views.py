from django.shortcuts import get_object_or_404, redirect, render
from django import template
from django.contrib.auth.decorators import permission_required, login_required
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny

from player.models import Deck, Player
from tournament.models import Match, Participant, Tournament
from tournament.serializers import ParticipantSerializer, TournamentSerializer
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
            date = request.POST.get("date")
        )
        tournament.save()
        tournament.create_tournament()
        return redirect(index, permanent=True)
    return HttpResponse(template.render(context, request))

def edit(request, id):
    template = loader.get_template('tournament/form.html')
    context = {}
    tournament = get_object_or_404(Tournament, pk = id)
    form = TournamentForm(tournament)
    context['edit'] = True
    context['tournament'] = tournament
    context['form'] = form
    if request.method == 'POST':
        tournament = Tournament(
            name = request.POST.get("name"),
            date = request.POST.get("date"),
            id_challonge = request.POST.get("id_challonge")
        )
        Tournament.objects.filter(pk = id).update(name=request.POST.get("name"), date=request.POST.get("date"), id_challonge=request.POST.get("id_challonge"))
        return redirect(index, permanent=True)
    return HttpResponse(template.render(context, request))

def view(request, id):
    template = loader.get_template('tournament/view.html')
    context = {}
    tournament = Tournament.objects.get(pk = id)
    context['tournament'] = tournament
    return HttpResponse(template.render(context, request))

def participant_view(request, id, participant):
    template = loader.get_template('tournament/participant/view.html')
    context = {}
    tournament = Tournament.objects.get(pk = id)
    participant = Participant.objects.get(pk = participant)
    decks = participant.player.getDecks()
    matchs1 = list(Match.objects.filter(tournament = tournament.pk, player1 = participant.pk))
    matchs2 = list(Match.objects.filter(tournament = tournament.pk, player2 = participant.pk))
    match = list()
    for m in matchs1:
        match.append(m)
    for m in matchs2:
        match.append(m)
    
    #[<Deck>, win, draw, loose]
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
        tournament.challonge_add_members()
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


def tournament_matchs_add(request, id):
    template = loader.get_template('tournament/match/add.html')
    context = {}
    tournament = get_object_or_404(Tournament, pk=id)
    if request.method == 'POST':
        
        match = Match(
            player1 = get_object_or_404(Participant, pk = request.POST.get("id_p1")),
            deck1 = get_object_or_404(Deck, pk = request.POST.get("decks1")),
            player2 = get_object_or_404(Participant, pk = request.POST.get("id_p2")),
            deck2 = get_object_or_404(Deck, pk = request.POST.get("decks2")),
            tournament = tournament
        )
        if request.POST.get("winner") == 'Winner':
            match.winner = get_object_or_404(Participant, pk = request.POST.get("id_p1"))
        elif request.POST.get("winner") == 'Looser':
            match.winner = get_object_or_404(Participant, pk = request.POST.get("id_p2"))
        match.save()
        return redirect(view, id)
    else:
        p1 = Participant.objects.get(pk = request.POST.get("id_p1"))
        p2 = Participant.objects.get(pk = request.POST.get("id_p2"))
        context['player1'] = p1
        context['player2'] = p2
        context['form'] = MatchForm(tournament, p1, p2)
        context['tournament'] = tournament
    return HttpResponse(template.render(context, request))

def timer(request):
    template = loader.get_template('other/timer.html')
    context = {}
    return HttpResponse(template.render(context, request))


class TournamentViewSet(viewsets.ModelViewSet):

    serializer_class = TournamentSerializer
    queryset = Tournament.objects.all()
    permission_classes = [
        IsAdminUser,
    ]
    @action(detail=True,methods=['post'])
    def start_challonge(self,request,pk=None):
        tournament = Tournament.objects.get(pk = pk)
        tournament.start_tournament()
        return redirect(view, pk)

    @action(detail=True,methods=['post'])
    def set_win(self,request,pk=None):
        winner = Participant.objects.get(pk =request.data["win"])
        looser = Participant.objects.get(pk =request.data["loose"])
        winner.set_win(looser)
        return redirect(view, pk)
from rest_framework.response import Response

class ParticipantViewSet(viewsets.ModelViewSet):

    serializer_class = ParticipantSerializer
    queryset = Participant.objects.all()
    permission_classes = [
        
    ]

        
    @action(detail=True,methods=['get'])
    def get_opponents(self,request,pk=None):
        participant = Participant.objects.get(pk=pk)
        opponents = participant.get_opponents()
        return Response(ParticipantSerializer( opponents,many=True).data)
        