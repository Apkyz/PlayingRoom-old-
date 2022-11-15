from datetime import datetime

from django import forms
from django.forms.widgets import DateInput, TextInput
from django.views.generic.edit import FormView

from .models import Item, Player


class ItemForm(forms.Form):
    """Form for an item"""
    name = forms.CharField(
        label='Name',
        required=True,
        widget= forms.TextInput(
            attrs={'class':'form-control'})
        )
    price = forms.DecimalField(
        label='Price',
        required=True,
        widget= forms.NumberInput(
            attrs={'class':'form-control', 'step':'0.01', 'min':0.01})
        )
    descr = forms.CharField(
        label='Description',
        required=False,
        widget= forms.Textarea(
            attrs={'class':'form-control', 'rows':4})
        )
    stock = forms.IntegerField(
        label='Stock',
        required=True,
        widget= forms.NumberInput(
            attrs={'class':'form-control', 'min':1})
        )
    
    def __init__(self, item:Item=None, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        if item:
            self.fields['name'].initial = item.name
            self.fields['price'].initial = item.price
            self.fields['descr'].initial = item.descr
            self.fields['stock'].initial = item.stock
        
