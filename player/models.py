from django.db import models

# Create your models here.

class Deck(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Player(models.Model):
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
    
class Match(models.Model):
    player1 = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='player1')
    deck1 = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='deck1')
    player2 = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='player2')
    deck2 = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='deck2')
    winner = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='winner')
    id_challonge = models.CharField(max_length=100)
    
class Tournament(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(blank=True, null=True)
    participants = models.ManyToManyField(Participant)
    matches = models.ManyToManyField(Match)
    id_challonge = models.URLField(max_length=100)
    
    def participants_count(self):
        return len(self.participants.all())
    def matches_count(self):
        return len(self.matches.all())