# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .forms import MyForm
from django.views.decorators.csrf import csrf_protect
import geocoder
import urllib
import xml.dom.minidom
import xml.etree.ElementTree as ET
import requests
import lxml.html
from bs4 import BeautifulSoup

ENCODING = 'utf-8'
@csrf_protect
def form_test(request):
	lat=35.689488
	lng=139.691706	  
        form = MyForm()
	return render(request, 'mapapp/index2.html',{
        'form': form,
        'lat': lat,
        'lng': lng,

    })


@csrf_protect
def test(request):
	index = "index.html"
	html = 0
	x = 0
	lat = 35.689488
	lng = 139.691706
	hotel = [" "] * 10
	hurl = [" "] * 10
	image = [" "] * 10
	price = [1]*10
	lat2 = [1] * 10
	lng2 = [1] * 10
	if request.method == "POST":
		form = MyForm(data=request.POST)

		if form.is_valid():
			w = request.POST['search']
			a = geocode(w)
			dom = xml.dom.minidom.parseString(a)
			location = dom.getElementsByTagName('location')
			if location.length > 0:
				lat = location[0].getElementsByTagName('lat')[0].firstChild.data
				lng = location[0].getElementsByTagName('lng')[0].firstChild.data
				html = jalan(lat, lng)
				hotel = result(html, 1)
				x = count(html, 1)
				hurl = result(html, 6)
				price = hprice(html)
				image = result(html, 9)
				hlocation = result(html, 3)
				htype = result(html,5)
				sss = scraping(hurl)
				for i in range(x):
					geo = geocode(hlocation[i + 1])
					dom = xml.dom.minidom.parseString(geo)
					location = dom.getElementsByTagName('location')
					if location.length > 0:
						lat2[i] = location[0].getElementsByTagName('lat')[0].firstChild.data
						lng2[i] = location[0].getElementsByTagName('lng')[0].firstChild.data
				if x == 3:
					index = "index3.html"
				else:
					index = "index.html"

	else:
		form = MyForm()
	if x == 3:
		return render(request, 'mapapp/%s' % index, {
			'form': form,
			'html': html,
			'lat': lat,
			'lng': lng,
			'a1': [hotel[1],hotel[2],hotel[3]],
			'a2': [hurl[1],hurl[2],hurl[3]],
			'b1': [image[1],image[2],image[3]],
			'c1': [lat2[0], lat2[1], lat2[2]],
			'c2': [lng2[0], lng2[1], lng2[2]],
			'd1': [price[1],price[2],price[3]],
			'e1': [hlocation[1],hlocation[2],hlocation[3]],
			'f1': [htype[1],htype[2],htype[3]]

		})
	else:
		return render(request, 'mapapp/%s' % index, {
			'form': form,
			'html': html,
			'lat': lat,
			'lng': lng,
			'a1': [hotel[1],hotel[2],hotel[3],hotel[4],hotel[5]],
			'a2': [hurl[1],hurl[2],hurl[3],hurl[4],hurl[5]],
			'b1': [image[1],image[2],image[3],image[4],image[5]],
			'c1': [lat2[0], lat2[1], lat2[2], lat2[3], lat2[4]],
			'c2': [lng2[0], lng2[1], lng2[2], lng2[3], lng2[4]],
			'd1': [price[1],price[2],price[3],price[4],price[5]],
			'e1': [hlocation[1],hlocation[2],hlocation[3],hlocation[4],hlocation[5]],
                        'f1': [htype[1],htype[2],htype[3],htype[4],htype[5]]

		})

def geocode(name):
	ENCODING = 'utf-8'
	url = u"http://maps.google.com/maps/api/geocode/xml?&language=ja&sensor=false&region=ja&address="

	url = url + urllib.quote(name.encode(ENCODING))
	
	buffer = urllib.urlopen(url).read()

	return buffer

def jalan(lat,lng):
	lat = float(lat) * 1.000106961 - float(lat) * 0.000017467 - 0.004602017
	lng = float(lng) * 1.000083049 + float(lng) * 0.000046047 - 0.010041046
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


def result(html,x):
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
			hotel.append(root[i][x].text)
			i+=1
	return hotel



def count(html,x):
        root=ET.fromstring(html)
        i=4
        hotel = ["A"]
	x=0
        for a in root:
                tag=a.tag
                if tag=="{jws}Hotel":
                        hotel.append(root[i][x].text)
                        i+=1
			x+=1
        return x

def hprice(html):
	root=ET.fromstring(html)
        i=4
	price = [" "]
        x=0
        for a in root:
                tag=a.tag
		tag2=a.tag
		x=0
                if tag=="{jws}Hotel":
                        while tag2 != "{jws}SampleRateFrom":
				x+=1
				tag2 = root[i][x].tag
			price.append(root[i][x].text)
			i+=1
        return price




def scraping(hurl):
	r = requests.get('%s'%hurl[1])
	#print(r.text)
	soup = BeautifulSoup(r.text,"lxml")
	
	for link in soup.find_all("link", rel="canonical"):
		purl=link['href']

	url = purl + "plan/"
	print(url)
	r = requests.get(url)
	soup = BeautifulSoup(r.text,"lxml")
	for tbody in soup.find_all("td", class_="s12_66"):
		print(tbody.text)
	return 5




	

