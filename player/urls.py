from django.shortcuts import render
from django.urls import path
from . import views

# Create your views here.

urlpatterns = [
    path('', views.index, name='player_index'),
    path('add/', views.add, name='player_add'),
    path('delete/<slug:cosy>/', views.delete, name='player_delete'),
    path('view/<slug:cosy>/', views.view, name='player_view'),
    path('edit/<slug:cosy>/', views.edit, name='player_edit'),
    
    path('decks/add/<slug:cosy>/', views.deck_add, name='player_deck_add'),
    path('decks/remove/<slug:cosy>/<slug:id>/', views.deck_remove, name='player_deck_remove'),
]