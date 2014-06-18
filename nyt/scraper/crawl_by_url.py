#!/usr/bin/python

# Use dev settings if not otherwise configured.
import parsers
from parsers.baseparser import canonicalize, formatter, logger

import os
import MySQLdb
import re

import requests
import urllib2
import httplib
import socket

import time

def main():
	os.system('sudo mysql -u root -ptoor nyt -e "DROP TABLE  IF EXISTS post_full;"')
	os.system('sudo mysql -u root -ptoor nyt -e "CREATE TABLE post_full(id BIGINT(20), url TEXT, article TEXT);"')
	db=MySQLdb.connect(host='localhost',user='root',passwd='toor',db='nyt')
	db.set_character_set('utf8')
	cur=db.cursor()

	cur.execute('SELECT Id,Message FROM post WHERE message IS NOT NULL AND YEAR(created_time)=2013;')
	for row in cur.fetchall():
		post_id=row[0]
		msg=row[1]
		try:
			article=''
			url=find_url(msg)
			if url:
				article=load_article(url)
				if article:
					article=article.body
				else:
					article=''
			else:
				url=''
		except Exception, e:
			logger.error('Failed to process post:%d'%post_id)
			logger.error('Failed url:%s'%url)
			logger.error(traceback.format_exc())
			time.sleep(10)
		finally:
			ins_cur=db.cursor()
			ins_cur.execute('INSERT INTO post_full(id,url,article) VALUES(%s,"%s","%s")',(str(post_id),url,article))
			db.commit()

def find_url(txt):
	try:
		regres=re.search("(?P<url>https?://[^\s]+)", txt)
	except Exception,e:
		logger.error('Failed to find url in %s'%txt)
		logger.error(e)
		return
	url=None
	if regres:
		url=regres.group("url")
	if not url:
		return None
	resp=requests.get(url)
	if not resp:
		return None
	real_url=resp.url
	return real_url

def load_article(url):
    try:
        parser = parsers.get_parser(url)
    except KeyError:
        logger.info('Unable to parse domain, skipping')
        return
    parsed_article = parser(url)
    if not parsed_article.real_article:
        return
    return parsed_article

if __name__ =='__main__':
	main()
