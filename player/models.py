from django.db import models

# Create your models here.

class Deck(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Player(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    cosy = models.CharField(max_length=20)
    decks = models.ManyToManyField(Deck, related_name='players')
    
    def __str__(self):
        return self.first_name + " " + self.last_name

class Championship(models.Model):
    name = models.CharField(max_length=100)
    players = models.ManyToManyField(Player)
    
RESULT_CHOICES = [
    
]
YEAR_IN_SCHOOL_CHOICES = [
    ('WIN', 'Gagner'),
    ('DRAW', 'Egalité'),
    ('LOOSE', 'Perdu'),
]
class Match(models.Model):
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player1')
    deck1 = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='deck1')
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player2')
    deck2 = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='deck2')
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='winner')
    result = models.CharField(choices=RESULT_CHOICES, max_length=5)
    