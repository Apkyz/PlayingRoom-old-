from player.models import Player
from django import forms
from django.forms.widgets import DateInput, TextInput
from datetime import datetime

from tournament.models import Participant, Tournament
    
class TournamentForm(forms.Form):
    name = forms.CharField(
        label='Name :',
        required=True,
        widget= forms.TextInput(
            attrs={'class':'form-control'})
        )
    
    date = forms.DateTimeField(
        initial=datetime.now,
        widget= forms.DateInput(
            attrs={'type':'date',
                   'class':'form-control'})
        )
    
    id_challonge = forms.URLField(
        label='Challonge :',
        required=False,
        min_length=0,
        widget= forms.TextInput(
            attrs={'class':'form-control'})
        )
    
    def __init__(self, tournament:Tournament=None, *args, **kwargs):
        super(TournamentForm, self).__init__(*args, **kwargs)
        if tournament:
            self.fields['name'].initial = tournament.name
            self.fields['date'].initial = tournament.date
            self.fields['id_challonge'].initial = tournament.id_challonge


class MatchForm(forms.Form):
    
    tournament = forms.CharField(
        label='tournament :',
        required=True,
        widget= forms.TextInput(
            attrs={'class':'form-control', 'type':'hidden'})
        )
    player1 = forms.CharField(
        label='player1 :',
        required=True,
        widget= forms.TextInput(
            attrs={'class':'form-control', 'type':'hidden'})
        )
    player2 = forms.CharField(
        label='player2 :',
        required=True,
        widget= forms.TextInput(
            attrs={'class':'form-control', 'type':'hidden'})
        )
        
    decks1 = forms.ChoiceField(
        label='decks1 :',
        required=True,
        widget= forms.Select(
            attrs={'class':'form-control'})
        )
    decks2 = forms.ChoiceField(
        label='decks2 :',
        required=True,
        widget= forms.Select(
            attrs={'class':'form-control'})
        )

    winner = forms.ChoiceField(
        label='Winner : ',
        required=True,
        widget= forms.Select(
            attrs={'class':'form-control'}),
        choices=[('Winner', 'Winner'), ('Looser', 'Looser'), ('Draw', 'Draw')])
    
    def __init__(self, tournament:Tournament=None, player1:Participant=None, player2:Participant=None, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        self.fields['tournament'].initial = tournament.pk
        self.fields['player1'].initial = player1.pk
        self.fields['player2'].initial = player2.pk
        if player1:
            decks = player1.player.getDecks()
            lst = [(deck.id, str(deck.name)) for deck in decks]
            self.fields['decks1'].choices = lst
        if player2:
            decks = player2.player.getDecks()
            lst = [(deck.id, str(deck.name)) for deck in decks]
            self.fields['decks2'].choices = lst