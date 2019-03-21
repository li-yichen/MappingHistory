#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

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

script_dir = os.path.dirname(__file__)

files = [f for f in listdir(script_dir+"/Data/") if isfile(join(script_dir+"/Data/", f))]

list_of_td_dict = []

for file in files:
	infile = open(script_dir+"/Data/"+file,"r")
	contents = infile.read()
	soup = BeautifulSoup(contents, "xml")

	entities = soup.find_all('Entity')

	for entity in entities:
		dict_of_td = {}
		td = entity.find('TopDisambiguation')
		if td.find('WikiTitle') and td.find('WikiTitleID'):
			wikititle = td.find('WikiTitle')
			wikititle = wikititle.get_text()
			dict_of_td["wikititle"] = wikititle
			wikiid = td.find('WikiTitleID')
			wikiid = wikiid.get_text()
			dict_of_td["wikiid"] = wikiid
			list_of_td_dict.append(dict_of_td)

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
	item["geo_lat"] = ""
	item["geo_long"] = ""
	wikititle = item["wikititle"]
	url = "https://en.wikipedia.org/wiki/" + wikititle
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	#if soup finds a <span> element in html with attribute 'class'="geo-dms",
	#which is where wikipedia shows the geo coordinates on top right corner
	#we use an if statement because the wiki may not have coordinates,
	#but if anyone better at programming were to rewrite this, they could change
	#it to something like "try blah blah blah"?
	if soup.find('span',{'class':"geo-dms"}):
		geo_span = soup.find('span',{'class':"geo-dms"})
		if geo_span.find('span',{'class':"latitude"}) and geo_span.find('span',{'class':"longitude"}):
			lat = geo_span.find('span',{'class':"latitude"})
			lat = lat.get_text()
			lon = geo_span.find('span',{'class':"longitude"})
			lon = lon.get_text()
			item["lat"] = lat
			item["lon"] = lon
f = open(script_dir+"/Data/"+'testxml.json','w',encoding='utf-8')
j = json.dumps(removed_duplicate_list_of_dict, indent=4)
f.write(j)
f.close()
