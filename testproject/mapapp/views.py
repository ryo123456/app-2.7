# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .forms import MyForm
import geocoder
import urllib
import xml.dom.minidom
import xml.etree.ElementTree as ET

ENCODING = 'utf-8'

def form_test(request):
        html=0
	lat=35.689488
	lng=139.691706
	hotel=["A"," "," "," "," "," "]
	hurl=["A"," "," "," "," "," "]
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
				html=jalan(lat,lng)
				hotel=result(html)
				hurl=hotelurl(html)
    	else:  
        	form = MyForm()
    	return render(request, 'mapapp/index.html', {
        'form': form,
        'html': html,
        'lat': lat,
        'lng': lng,
	'a1' : hotel[1],
	'a2' : hotel[2],
	'a3' : hotel[3],
	'a4' : hotel[4],
	'a5' : hotel[5],
	'a6' : hurl[1],
	'a7' : hurl[2],
	'a8' : hurl[3],
	'a9' : hurl[4],
	'a10' : hurl[5],
        
    })

def geocode(name):
	ENCODING = 'utf-8'
	url = u"http://maps.google.com/maps/api/geocode/xml?&language=ja&sensor=false&region=ja&address="

	url = url + urllib.quote(name.encode(ENCODING))

	buffer = urllib.urlopen(url).read()

	return buffer

def jalan(lat,lng):
	lat = float(lat) * 1.000106961 - float(lng) * 0.000017467 - 0.004602017
	lng = float(lng) * 1.000083049 + float(lat) * 0.000046047 - 0.010041046
	lat = lat * 3600 * 1000
	lng = lng * 3600 * 1000
	lat = int(lat)
	lng = int(lng)
	url = "http://jws.jalan.net/APIAdvance/HotelSearch/V1/"
	api_key = "and15e316b9f30"
	range = 10
	url = url +  "?order=4&xml_ptn=1&pict_size=0&key=" + api_key + "&x=" + str(lng) +"&y=" + str(lat) + "&range=" + str(range)
	html = urllib.urlopen(url).read()
	
	return html


def result(html):
	#f = open('mapapp/templates/mapapp/test.xml','w')
	#f.write(html)
	#f.close()
	#tree=ET.parse('mapapp/templates/mapapp/test.xml')
	#root=tree.getroot()
	root=ET.fromstring(html)
	#a=root.findtext("HotelAddress")
	i=4
	hotel = ["A"]
	for a in root:
		tag=a.tag
		if tag=="{jws}Hotel":
			print (root[i][1].text)
			hotel.append(root[i][1].text)
			i+=1
	return hotel

def hotelurl(html):
        root=ET.fromstring(html)
        i=4
        hurl = ["A"]
        for a in root:
                tag=a.tag
                if tag=="{jws}Hotel":
                        #print (root[i][6].text)
                        hurl.append(root[i][6].text)
                        i+=1
        return hurl
