from .models import Player
from django import forms
from django.forms.widgets import DateInput, TextInput
from django.views.generic.edit import FormView
from datetime import datetime
from django.contrib.auth.models import User

class PlayerForm(forms.Form):
    user = forms.ChoiceField(
        label='user :',
        required=True,
        widget= forms.Select(
            attrs={'class':'form-control'})
        )
    first_name = forms.CharField(
        label='First name :',
        required=True,
        widget= forms.TextInput(
            attrs={'class':'form-control'})
        )
    
    last_name = forms.CharField(
        label='Last name :',
        required=True,
        widget= forms.TextInput(
            attrs={'class':'form-control'})
        )
    cosy = forms.CharField(
        label='Cosy :',
        min_length=0,
        max_length=10,
        required=True,
        widget= forms.TextInput(
            attrs={'class':'form-control'})
        )
    
    def __init__(self,  user:User, player:Player=None, *args, **kwargs):
        super(PlayerForm, self).__init__(*args, **kwargs)
        if player:
            self.fields['first_name'].initial = player.first_name
            self.fields['last_name'].initial = player.last_name
            self.fields['cosy'].initial = player.cosy
        if user.is_staff:
            users = User.objects.all()
            self.fields['user'].choices = [(user.id, str(user.username)) for user in users]
        else:
            users = list(User.objects.filter(username = user.username))
            self.fields['user'].choices = [(user.id, str(user.username)) for user in users]
    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        cosy = cleaned_data.get("cosy")
        
