from django.db import models
from django.conf import settings
import requests

from player.models import Deck, Player


class Participant(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player')
    payed = models.BooleanField()
    id_challonge = models.CharField(max_length=100)
    def __str__(self):
        return str(self.player) + " " + str(self.payed)
    
class Tournament(models.Model):
    
    _challonge_url = "https://challonge.com/fr/"
    __challonge_api_url =f"https://appez@api.challonge.com/v1/tournaments"

    _header = {
            "Content-Type": "application/json",
            "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
        }

    __params = {
            "api_key" : settings.CHALLONGE_TOKEN
        }

    name = models.CharField(max_length=100)
    date = models.DateField(blank=True, null=True)
    participants = models.ManyToManyField(Participant)
    id_challonge = models.CharField(max_length=100,blank=True, null=True)
    
    def participants_count(self):
        return len(self.participants.all())
    def match_count(self):
        return len(Match.objects.filter(tournament = self.pk))

    def create_tournament(self):


        data = {
            "tournament" : {
                "name" : self.name,
                "tournament_type" : "swiss",
                "open_signup" : "false",
                "private"  : "true",
                "game-id" : 45,
                "game_name" : "Yu-Gi-Oh!",
            }
        }

        response = requests.post(
            self.__challonge_api_url+".json",
            headers=self._header,
            json=data,
            params=self.__params
        )
        
        if(response.status_code == 200):
            self.id_challonge = response.json()['tournament']["url"]
        print(self.__params)
        print(response)
    
class Match(models.Model):
    player1 = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='player1')
    deck1 = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='deck1')
    player2 = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='player2')
    deck2 = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='deck2')
    winner = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='winner', blank=True, null=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='tournament')
    
    def __str__(self):
        msg = "[MATCH] " + str(self.player1.player) + " " + str(self.deck1) + " || " + str(self.player2.player) + " " + str(self.deck2) + " || WINNER : " + str(self.winner.player)
        return msg
    def getWinnerDeck(self):
        if self.winner == self.player1:
            return self.deck1
        elif self.winner == self.player2:
            return self.deck2
        else:
            return None 
    def getResult(self, participant):
        if self.winner == None:
            return 'draw'
        elif self.winner == participant:
            return 'win'
        else:
            return 'loose'
            