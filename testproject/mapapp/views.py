# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .forms import MyForm
# Create your views here.
#def index(request):
   # return render(request, 'mapapp/index.html')

def form_test(request):
    form = MyForm()
    return render(request, 'mapapp/index.html', {
        'form': form,
    })
