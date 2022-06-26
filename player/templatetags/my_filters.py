from django import template

register = template.Library()

@register.filter
def first_upper(value):
    stri = str(value)
    modif = stri.capitalize()
    return modif