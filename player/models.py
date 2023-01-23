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

