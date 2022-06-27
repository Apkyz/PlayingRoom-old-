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
]