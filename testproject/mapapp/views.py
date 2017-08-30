# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .forms import MyForm
import geocoder
import urllib
import xml.dom.minidom
def form_test(request):
    	if request.method == "POST":
        	form = MyForm(data=request.POST)  
        	if form.is_valid():  
            		w=request.POST['text']
			a=geocode(w)
			dom = xml.dom.minidom.parseString(a)
			location = dom.getElementsByTagName('location')
			if location.length > 0:
        			lat = location[0].getElementsByTagName('lat')[0].firstChild.data
        			lng = location[0].getElementsByTagName('lng')[0].firstChild.data
				print(lat,lng)	
		 
    	else:  
        	form = MyForm()
    	return render(request, 'mapapp/index.html', {
        'form': form,
    })

def geocode(name):
	ENCODING = 'utf-8'
	url = u"http://maps.google.com/maps/api/geocode/xml?&language=ja&sensor=false&region=ja&address="

	url = url + urllib.quote(name.encode(ENCODING))

	buffer = urllib.urlopen(url).read()

	return buffer


