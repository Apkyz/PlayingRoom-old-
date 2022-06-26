from django.shortcuts import render
from django.urls import path
from . import views

# Create your views here.

urlpatterns = [
    path('', views.index, name='player_index'),
    path('add/', views.add, name='player_add'),
]