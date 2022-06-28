from django.db import models

# Create your models here.

class Deck(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Player(models.Model):
    cosy = models.CharField(max_length=20, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    decks = models.ManyToManyField(Deck, related_name='players')
    
    def __str__(self):
        return self.first_name + " " + self.last_name

class Participant(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player')
    payed = models.BooleanField()
    
class Tournament(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(blank=True, null=True)
    participant = models.ManyToManyField(Participant)
    
class Match(models.Model):
    player1 = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='player1')
    deck1 = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='deck1')
    player2 = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='player2')
    deck2 = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='deck2')
    winner = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='winner')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='tournament')
