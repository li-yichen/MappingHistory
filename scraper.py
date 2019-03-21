#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import requests
import time
from bs4 import BeautifulSoup
import os

script_dir = os.path.dirname(__file__)


#looping thru years not successful
#for i in range (201,2013):
year = 2012
byyear_url = 'http://jsah.ucpress.edu/content/by/year/'+str(year)

#byyear_url = 'http://jsah.ucpress.edu/content/by/year/2015'
response = requests.get(byyear_url)
soup = BeautifulSoup(response.text, "html.parser")

if soup.find_all('div',{'class':"issue-link"}):
	issue_links = soup.find_all('div',{'class':"issue-link"})
#elif soup.find_all('a',{'class':"issue-link"}):
#	issue_links = soup.find_all('a',{'class':"issue-link"})
#else:
	#continue

for issue_link in issue_links:
	if issue_link.find('a'):
		i_link = issue_link.find('a')
	else:
		i_link = issue_link
	i_link = i_link.get('href')
	i_complete_link = "http://jsah.ucpress.edu"+i_link
	i_response = requests.get(i_complete_link)
	i_soup = BeautifulSoup(i_response.text, "html.parser")

	#print(i_complete_link)
	
	#due to the chaos in html formatting among issues throughout the years, we go
	#through all the possible ways to find the article list
	if i_soup.find('li',{'class':"odd issue-toc-section issue-toc-section-articles"}):
		article_section = i_soup.find('li',{'class':"odd issue-toc-section issue-toc-section-articles"})
	elif i_soup.find('li',{'class':"even issue-toc-section issue-toc-section-articles"}):
		article_section = i_soup.find('li',{'class':"even issue-toc-section issue-toc-section-articles"})
	elif i_soup.find('div',{'class':"issue-toc-section issue-toc-section-articles"}):
		article_section = i_soup.find('div',{'class':"issue-toc-section issue-toc-section-articles"})
	elif i_soup.find('div',{'class':"issue-toc-section issue-toc-section-article"}):
		article_section = i_soup.find('div',{'class':"issue-toc-section issue-toc-section-article"})
	else:
		continue

	#print(article_section)

	article_links = article_section.find_all('a',{'class':"highwire-cite-linked-title"})

	for article_link in article_links:
		a_link = article_link.get('href')

		print(a_link)
		a_complete_link = "http://jsah.ucpress.edu/"+a_link
		a_response = requests.get(a_complete_link)
		a_soup = BeautifulSoup(a_response.text, "html.parser")

		if a_soup.find('div',{'class':"highwire-cite-title", 'id':"page-title"}):
			a_title = a_soup.find('div',{'class':"highwire-cite-title", 'id':"page-title"})
			a_title = a_title.get_text()
		elif a_soup.find('div',{'class':"highwire-cite-title title-with-subtitle", 'id':"page-title"}):
			a_title = a_soup.find('div',{'class':"highwire-cite-title title-with-subtitle", 'id':"page-title"})
		if a_soup.find('div',{'class':"highwire-cite-subtitle"}):
				a_title += " "+(a_soup.find('div',{'class':"highwire-cite-subtitle"}).get_text())

		a_paragraphs = a_soup.find_all('p')

		a_doi = a_soup.find('span',{'class':"highwire-cite-metadata-doi highwire-cite-metadata"})
		a_doi = a_doi.get_text()
		a_doi = a_doi[18:-1]
		print(a_doi)

		with open(script_dir+"/"+a_doi+".txt","w",encoding="utf-8") as f:
			f.write(a_title+'\n')
			for a_p in a_paragraphs:
				a_p = a_p.get_text()
				f.write(a_p+'\n')