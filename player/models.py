from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Deck(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cosy = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    decks = models.ManyToManyField(Deck, related_name='players')
    
    def __str__(self):
        return self.first_name + " " + self.last_name
    def getDecks(self):
        return list(self.decks.all())

class Participant(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player')
    payed = models.BooleanField()
    id_challonge = models.CharField(max_length=100)
    def __str__(self):
        return str(self.player) + " " + str(self.payed)
    
class Tournament(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(blank=True, null=True)
    participants = models.ManyToManyField(Participant)
    id_challonge = models.URLField(max_length=100)
    
    def participants_count(self):
        return len(self.participants.all())
    def match_count(self):
        return len(Match.objects.filter(tournament = self.pk))
    
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
            