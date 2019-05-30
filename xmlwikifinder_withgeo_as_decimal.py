#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

# finds geo-coordinates (in decimal format) from Wikified outputs (xml)

import time
import requests
from bs4 import BeautifulSoup
import os
import lxml
from collections import Counter
import json
import string

from os import listdir
from os.path import isfile, join

#on mac, the below line needs to be changed to:
script_dir = os.path.dirname(__file__)
#on linux, after cd-ing to the current dir, the above line needs to be changed to:
#script_dir = os.getcwd()

files = [f for f in listdir(script_dir+"/Data/") if isfile(join(script_dir+"/Data/", f))]

list_of_td_dict = []

for file in files:
	infile = open(script_dir+"/Data/"+file,"r")
	print(file)
	contents = infile.read()
	soup = BeautifulSoup(contents, "xml")

	entities = soup.find_all('Entity')

	#2019/05/28: find title of article, only tested on JSAH!
	inputtext = soup.find('InputText').get_text()
	inputtextlines = inputtext.splitlines()
	article = ': '.join(inputtextlines[1:3])
	print(article)

	for entity in entities:
		dict_of_td = {}
		dict_of_td["article"] = []
		#2019/05/28: added Rankerscore filter, idea and function credit: Dr.Baciu
		if float(entity.find('LinkerScore').get_text()) >=0.8:
			ls = float(entity.find('LinkerScore').get_text())
			td = entity.find('TopDisambiguation')
			if td.find('WikiTitle') and td.find('WikiTitleID'):
				#same as above, makes sure linkerscore > 0.5 and linkerscore x rankerscore > 0.5
				if (td.find('RankerScore') and (float(td.find('RankerScore').get_text())>= 0.5) and (float(td.find('RankerScore').get_text())*ls >= 0.5)):
					#2019/05/28: adds article field as a list of string of articles it involves
					dict_of_td["article"].append(article)
					#print(dict_of_td["article"])
					wikititle = td.find('WikiTitle')
					wikititle = wikititle.get_text()
					#print(wikititle)
					dict_of_td["wikititle"] = wikititle
					wikiid = td.find('WikiTitleID')
					wikiid = wikiid.get_text()
					dict_of_td["wikiid"] = wikiid
					list_of_td_dict.append(dict_of_td)
					#print(dict_of_td)

#counts occurances of wikipedia ids in the previous dictionary, makes
#a new dictionary that has {wikiid:count, wikiid:count, wikiid:count, ...} format
dict_of_count = {}
wikititles = Counter(k['wikititle'] for k in list_of_td_dict if k.get('wikititle'))
for wikiid, count in wikititles.most_common():
	dict_of_count.update({wikiid : count})
	#print(dict_of_count)

for each_td_dict in list_of_td_dict:
	wikititle = each_td_dict["wikititle"]
	each_td_dict["count"] = dict_of_count.get(wikititle)

removed_duplicate_list_of_dict = [i for n, i in enumerate(list_of_td_dict) if i not in list_of_td_dict[n + 1:]] 


for item in removed_duplicate_list_of_dict:
	wikititle = item["wikititle"]
	url = "https://en.wikipedia.org/wiki/" + wikititle
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	#if soup finds a <span> element in html with attribute 'class'="geo-dms",
	#which is where wikipedia shows the geo coordinates on top right corner
	#we use an if statement because the wiki may not have coordinates,
	#but if anyone better at programming were to rewrite this, they could change
	#it to something like "try blah blah blah"?
	if soup.find('span',{'class':"geo-nondefault"}):
		geo_span = soup.find('span',{'class':"geo-nondefault"})
		if geo_span.find('span',{'class':"geo-dec"}):
			latlon = geo_span.find('span',{'class':"geo-dec"})
			latlon = latlon.get_text()
			lat = latlon.split(" ")[0];
			lon = latlon.split(" ")[1];
			if "N" in lat:
				lat = float(lat[:-2])
			elif "S" in lat:
				lat = float(lat[:-2])
				lat = lat*(-1)
			if "E" in lon:
				lon = float(lon[:-2])
			elif "W" in lon:
				lon = float(lon[:-2])
				lon = lon*(-1)
			coord = (lat,lon)
			item["lat"] = lat
			item["lon"] = lon
#here is where the output file name could be changed:
f = open(script_dir+'/testxml.json','w+',encoding='utf-8')
j = json.dumps(removed_duplicate_list_of_dict, indent=4)
f.write(j)
f.close()
