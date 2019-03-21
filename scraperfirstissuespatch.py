import requests
import time
from bs4 import BeautifulSoup
import os

script_dir = os.path.dirname(__file__)

i_link = "/content/67/1"
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
	print(a_paragraphs)

	a_doi = a_soup.find('span',{'class':"highwire-cite-metadata-doi highwire-cite-metadata"})
	a_doi = a_doi.get_text()
	a_doi = a_doi[18:-1]

	with open(script_dir+"/"+a_doi+".txt","w",encoding="utf-8") as f:
		f.write(a_title+'\n')
		for a_p in a_paragraphs:
			a_p = a_p.get_text()
			f.write(a_p+'\n')