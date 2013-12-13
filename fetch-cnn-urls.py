import csv
import re
import sys
import urllib2
import httplib
import urlparse
import time
import codecs
import os.path
import random

from optparse import OptionParser

import feedparser
from bs4 import BeautifulSoup, Comment, Tag

def fetch_cnn(url):
	
	try:
		response = urllib2.urlopen(url)
	except urllib2.URLError:
		return None, None, None
	except Exception:
		return None, None, '<socketerror>'
	
	if response.getcode() <> 200:
		return None, None, '<httperror'+str(response.getcode) + '>'

	page=''
	while True:
		data=response.read()
		if not data:break
		page+=data
	
	soup = BeautifulSoup(page)
	title = scrape_title(soup)
	#highlights = scrape_highlights(soup)
	highlights=[]
	content = scrape_content(soup)	
	return title, highlights, content

def scrape_title(soup):
	rc = soup.find('div', id='cnnContentContainer')
	title=None
	if rc and rc.h1 and rc.h1.string:
		title = rc.h1.string.strip()
	return title
	
def scrape_content(soup):
	txt = soup.find('div', attrs={"class":'cnnContentContainer'})
	if not txt:
			txt = soup.find('div', attrs={"class":'cnn_storyarea'})
	if not txt:
			txt = soup.find('div', attrs={"class":'cnnContent'})
	if not txt:
		return None
	#remove as much junk from the content part as possible
	[tag.extract() for tag in txt.findAll(attrs={"class" : "cnn_strylctcntr"})]
	[tag.extract() for tag in txt.findAll(attrs={"class" : "cnn_strylftcntnt"})]
	[tag.extract() for tag in txt.findAll(attrs={"class" : "cnnStryVidCont"})]
	[tag.extract() for tag in txt.findAll(attrs={"class" : "cnn_strybtntoolsbttm"})]
	[tag.extract() for tag in txt.findAll(attrs={"class" : "cnn_strybtmcntnt"})]
	
	paragraphs = txt.findAll('p', recursive=False)
	result = []
	for paragraph in paragraphs:
		content = scrape_text(paragraph)
		content = content.strip("\n")
		if content.strip() != "":
			result.append(content.strip())
 
	return result

def scrape_text(content):
	#scrapes the text from an element.
	#removes comments
	#removes <tag>NEW:</tag>
	#removes <tag>*(CNN)</tag>
	#removes -- at start of text
	result = []
	for item in content:
		if isinstance(item, Comment):
			continue
		if not item.string:
			continue
		if isinstance(item, Tag):
			if item.string.strip() == "NEW:":
				continue
			if item.string.strip().endswith('(CNN)'):
				continue
		#if all blank space but more than one character
		if item.string.strip() == "" and len(item.string) > 1:
			continue
		if item.string.strip().startswith('--'):
			item.string = item.string.strip()[2:]
		result.append(item.string)
	return "".join(result)

#def main():
startid=None
startid='471020246508'
with open('/tmp/cnn-comm-ispost-msg.csv') as csvfile:
	rdr = csv.reader(csvfile,delimiter="\t")
		
	for row in rdr:		
		fbid=row[0]
		ispost=row[1]
		message=row[3]
		
		if startid and fbid != startid: continue
		else: startid = None
			
		if not ispost: continue

		regres=re.search("(?P<url>https?://[^\s]+)", message)
		if regres:
			url=regres.group("url")
			_, _, content = fetch_cnn(url)
			if content:
				fultext=' '.join([p.encode('ascii','ignore') for p in content])
			else:
				fultext='\N'
		else:
			url='\N'
			fultext='\N'
		
		row[4]=url
		row[5]=fultext
		
		output= "\t".join(row)
		print output
		
'''
if __name__=='__main__':
	sys.exit(main)
'''

