from django.shortcuts import render
from django.urls import path
from . import views

# Create your views here.

urlpatterns = [
    path('', views.index, name='tournament_index'),
    path('add/', views.add, name='tournament_add'),
    path('edit/<slug:id>/', views.edit, name='tournament_edit'),
    path('timer/', views.timer, name='timer'),
    path('add/participant/<slug:id>/', views.participant_add, name='tournament_participant_add'),
    path('participant/edit/', views.participant_edit, name='tournament_participant_edit'),
    
    path('<slug:id>/add/matches/', views.tournament_matchs_add, name='tournament_matchs_add'),
    path('<slug:id>/add/matches/<slug:id_p1>/', views.tournament_matchs_add, name='tournament_matchs_add'),
    path('<slug:id>/add/matches/<slug:id_p1>/<slug:id_p2>/', views.tournament_matchs_add, name='tournament_matchs_add_load_deck'),
    path('<slug:id_t>/participant_update/<int:id>', views.participant_update, name='tournament_participant_update'),

    path('<int:pk>/start_challonge',view=views.TournamentViewSet.as_view({'post': 'start_challonge'}),name='start_challonge'),
    path('<int:pk>/participant/set_win',view=views.ParticipantViewSet.as_view({'post': 'set_win'}),name='set_win'),
    path('<slug:id>/<slug:participant>/', view=views.participant_view, name='tournament_participant_view'),
    path('<slug:id>/', views.view, name='tournament_view'),

]
