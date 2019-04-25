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

#sets up a variable that is the path to the current directory, so file can be moved among different computers.
script_dir = os.path.dirname(__file__)

#on linux computers, the above line needs to be changed to:
# script_dir = os.getcwd()

#data should be stored within "Data" folder within current directory, "files" is all files in that folder.
files = [f for f in listdir(script_dir+"/Data/") if isfile(join(script_dir+"/Data/", f))]

#makes a list of dictionaries to store the information of each article (each is one dictionary).
list_of_td_dict = []

#for each file in previously defined "files"
for file in files:
	#we open this file, read it, and then set up a Beautifulsoup thing from this file's contents
	infile = open(script_dir+"/Data/"+file,"r")
	contents = infile.read()
	soup = BeautifulSoup(contents, "xml")
	
	#finds all the "Entity" tags in the xml file.
	entities = soup.find_all('Entity')
	
	#for each "Entity" tag
	for entity in entities:
		#make a dictionary
		dict_of_td = {}
		#find "TopDisambiguation" of each Entity
		td = entity.find('TopDisambiguation')
		#find "Wikititle" and "WikiTitleID" of each TopDisambiguation.
		if td.find('WikiTitle') and td.find('WikiTitleID'):
			#start defining some variables, i.e. wikititle.
			wikititle = td.find('WikiTitle')
			wikititle = wikititle.get_text()
			#defines "wikititle" for our dictionary.
			dict_of_td["wikititle"] = wikititle
			wikiid = td.find('WikiTitleID')
			wikiid = wikiid.get_text()
			#defines "wikiid" for our dictionary.
			dict_of_td["wikiid"] = wikiid
			#adds current dictionary to list of dictionaries.
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
	
#removes duplicate stuff, makes new dictionary out of non-repeating entities, with "count" column.
removed_duplicate_list_of_dict = [i for n, i in enumerate(list_of_td_dict) if i not in list_of_td_dict[n + 1:]] 

#scrapes geo coordinates off wikipedia, also with beautifulsoup.
for item in removed_duplicate_list_of_dict:
	item["geo_lat"] = ""
	item["geo_long"] = ""
	wikititle = item["wikititle"]
	url = "https://en.wikipedia.org/wiki/" + wikititle
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	#we use an if statement because the wiki may not have coordinates,
	#but if anyone better at programming were to rewrite this, maybe they could change
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
#dump everything in json
f = open(script_dir+"/Data/"+'testxml.json','w',encoding='utf-8')
j = json.dumps(removed_duplicate_list_of_dict, indent=4)
f.write(j)
f.close()
