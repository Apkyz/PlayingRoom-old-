from django.shortcuts import render
from django.urls import path
from . import views

# Create your views here.

urlpatterns = [
    path('', views.index, name='cashregister_index'),
    
    path('add/item/', views.add_item, name='cashregister_add_item'),
    path('delete/item/<slug:id>/', views.delete_item, name='cashregister_delete_item'),
    path('view/item/<slug:id>/', views.view_item, name='cashregister_view_item'),
]