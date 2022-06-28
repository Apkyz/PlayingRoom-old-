from operator import mod
from django.db import models

from player.models import Player

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    descr = models.CharField(max_length=500)
    stock = models.IntegerField()
    
    def __str__(self):
        return self.name + " " + str(self.price)

class Bill(models.Model):
    items = models.ManyToManyField(Item)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField()
    
    def total(self):
        total : float = 0
        for i in self.items.all:
            total += float(i.price)
        return total