#!/bin/python

import os
import csv
import MySQLdb
from urlparse import urlparse

os.system('sudo mysql -u root -ptoor nyt -e "DROP TABLE  IF EXISTS tags;"')
os.system('sudo mysql -u root -ptoor nyt -e "CREATE TABLE tags(url TEXT, tags TEXT);"')

url_tags={}
with open('/tmp/nyt/socialbm0311/nyt_tags.tsv','r') as f:
	reader=csv.reader(f,delimiter='\t')
	for row in reader:
		try:
			url_compos=urlparse(row[2])
		except Exception,e:
			print e
			print 'Error at'
			print row
			continue
		url=url_compos.scheme + '://' + url_compos.netloc + url_compos.path
		tags=set([])
		if len(row)>=6:
			tags=set(row[5:])
		if url in url_tags:
			url_tags[url]=url_tags[url].union(tags)
		else:
			url_tags[url]=tags

db=MySQLdb.connect(host='localhost',user='root',passwd='toor',db='nyt')
ins_cur=db.cursor()

for url,tags in url_tags.items():
	tags="><".join(tags)
	tags="<"+tags+">"
	ins_cur.execute('INSERT INTO tags(url,tags) VALUES("%s","%s")',(url,tags))

db.commit()

