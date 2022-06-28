from django.shortcuts import get_object_or_404, redirect, render
from django import template
from django.contrib.auth.decorators import permission_required, login_required
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect

from .forms import ItemForm
from .models import Item, Bill
# Create your views here.

@login_required(login_url="/login/")
def index(request):
    template = loader.get_template('cash/index.html')
    context = {}
    
    items = Item.objects.all()
    context['items'] = items
    context['segment'] = 'cashregister_index'
    return HttpResponse(template.render(context, request))

def add_item(request):
    template = loader.get_template('cash/item_add.html')
    context = {}
    if request.method == 'POST':
        item = Item(
            name=request.POST.get("name"),
            price=request.POST.get("price"),
            descr = request.POST.get("descr"),
            stock = request.POST.get("stock"))
        print(item)
        item.save()
        return redirect(index, permanent=True)
    else:
        form = ItemForm()
    context['form'] = form
    return HttpResponse(template.render(context, request))

def delete_item(request, id):
    print(id)
    item = get_object_or_404(Item, pk=id)
    
    item.delete()
    return redirect(index, permanent=True)


def view_item(request, id):
    return redirect(index, permanent=True)