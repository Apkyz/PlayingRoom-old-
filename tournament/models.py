from django.db import models
from django.conf import settings
import requests

from player.models import Deck, Player

CHALLONGE_URL = "https://challonge.com/fr/"
CHALLONGE_API_URL =f"https://appez@api.challonge.com/v1/tournaments"

HEADER = {
        "Content-Type": "application/json",
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    }

PARAMS = {
        "api_key" : settings.CHALLONGE_TOKEN
    }

class Participant(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player')
    payed = models.BooleanField()
    id_challonge = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return str(self.player) + " " + str(self.payed)

    def get_opponents(self):

        opponents = []

        tournament = Tournament.objects.get(participants__pk = self.pk)

        params = PARAMS
        params['state'] = 'open'
        params['participant_id'] = self.id_challonge

        response = requests.get(
            CHALLONGE_API_URL+f"/{tournament.id_challonge}/matches.json",
            headers=HEADER,
            params=params
        )


        
        if response.status_code == 200:
            matches = response.json()

            for match in matches:
                match_data = match['match']

                if tournament.first_part:
                    if tournament.participants_count() % 2 == 0:
                        nb_round = (tournament.participants_count()-1)
                    else :
                         nb_round = tournament.participants_count()
                    if match_data['round'] > nb_round:
                        continue
                if str(match_data['player1_id']) ==self.id_challonge:
                    id_opp =  match_data['player2_id']
                else :
                    id_opp =  match_data['player1_id']
                
                opponent = Participant.objects.get(id_challonge = id_opp)

                opponents.append(opponent)
        return opponents

    def set_win(self,opponent):
        print("ok")
    
class Tournament(models.Model):
    

    name = models.CharField(max_length=100)
    date = models.DateField(blank=True, null=True)
    participants = models.ManyToManyField(Participant)
    id_challonge = models.CharField(max_length=100,blank=True, null=True)
    is_started = models.BooleanField(default=False)
    first_part = models.BooleanField(default=True)

    def participants_count(self):
        return len(self.participants.all())
    def match_count(self):
        return len(Match.objects.filter(tournament = self.pk))

    def create_tournament(self):


        data = {
            "tournament" : {
                "name" : self.name,
                "tournament_type" : "round robin",
                "open_signup" : "false",
                "ranked_by" : "points scored",
                "rr_iterations" : 2,
                "private"  : "true",
                "game-id" : 45,
                "game_name" : "Yu-Gi-Oh!",
            }
        }

        response = requests.post(
            CHALLONGE_API_URL+".json",
            headers=HEADER,
            json=data,
            params=PARAMS
        )
        
        if(response.status_code == 200):
            self.id_challonge = response.json()['tournament']["url"]
            self.save()

    def challonge_add_members(self):
        duelists = []
        members = self.participants.filter(id_challonge = '')
        for member in members:
            duelists.append({"name": f"{member.player.first_name} {member.player.last_name}"})

        data = {
            "participants" : duelists,
        }  
        response = requests.post(
            CHALLONGE_API_URL+f"/{self.id_challonge}/participants/bulk_add.json",
            headers=HEADER,
            json=data,
            params=PARAMS
        )
        if response.status_code == 200:
            for index,duelist in enumerate(response.json()):
                members[index].id_challonge = duelist["participant"]["id"]
                members[index].save()

    def start_tournament(self):
        requests.post(
            CHALLONGE_API_URL+f"/{self.id_challonge}/participants/randomize.json",
            headers=HEADER,
            params=PARAMS
        )

        response = requests.post(
            CHALLONGE_API_URL+f"/{self.id_challonge}/start.json",
            headers=HEADER,
            params=PARAMS
        )

        if response.status_code == 200:
            self.is_started = True
            self.save()

            
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
            