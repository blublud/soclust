from igraph import *
import csv
import re
import time

import sys; sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/byweek_stats/'); import alchemyapi

#csv format
#post_id	message	created_time	yearweek

POST_ID=0
MESSAGE=1
CREATED_TIME=2
YEARWEEK=3
WORD_CLOUD=4
props=[
	'post_id',
	'message',
	'created_time',
	'yearweek',
	'word_cloud'#newly-added
]

def getTextFromGraph(g, vertices=None,textproperty='text'):

	if vertices:
		g=g.induced_subgraph(vertices,implementation='create_from_scratch')
	
	texts=[vdoc[textproperty] for vdoc in g.vs if textproperty in vdoc]
	return texts

def loadTextFromFile(f_text):
	
	texts={}
	with open(f_text,'rb') as f:
		reader=csv.reader(f,delimiter="\t", quoting=csv.QUOTE_NONE)
		for row in [row for row in reader if row[0][0]!='#']:
			message=row[MESSAGE].decode('ascii','ignore')
			texts[row[POST_ID]]=message

	return texts

def getWordClouds(texts):
	wordClouds={}
	
	for textId in sorted(texts):
		content=texts[textId]
		try:
			wordCloud=getWordCloud(content)
			wordClouds[textId]=wordCloud
		except Exception, err:
			sys.stderr.write('Error at textId %s.Details:%s'%(textId,str(err)))
			return wordClouds

	return wordClouds

def saveWordClouds(wordClouds,f_wordCloud):
	with open(f_wordCloud,'wb') as f:
		writer=csv.writer(f,delimiter="\t")
		writer.writerow(['#docId','entities','keyWords'])
		for textId in sorted(wordClouds):
			(entities,keywords)=wordClouds[textId]
			row=[textId,entities,keywords]
			writer.writerow(row)

def getWordCloud(text):
	text=re.sub(r'https?://\S+','',text)
	text=re.sub('\.+','.',text)
	text=re.sub('!','',text)
	if len(text)<10: 
		return ('','')
	else:
		(entities,keywords)=getEntitiesKeywords(text)	
		return (';'.join(entities),';'.join(keywords))
	
def loadTextToGraph(g, texts,textproperty='text'):

	for vdoc in [vdoc for vdoc in g.vs if vdoc['name'][0]=='p']:
		vdoc[textproperty]=texts[vdoc['name']]

def loadWordCloudToGraph(g,wordClouds,entities_prop='ent',keywords_prop='keyw'):
	for vdoc in [vdoc for vdoc in g.vs if vdoc['name'][0]=='p']:
		wordCloud=wordClouds[vdoc['name']]
		if wordCloud is not None:
			(entities,keywords)=wordCloud
			vdoc[entities_prop]=';'.join(entities)
			vdoc[keywords_prop]=';'.join(keywords)

def getEntitiesKeywords(text):
	api = alchemyapi.AlchemyAPI()
	response = api.entities('text',text, { 'sentiment':1 })
	if  response['status']!='OK':
		raise Exception('Error from alchemy.\nText:%s\nStatus is:%s\nResponse:%s'%(text,response['status'],response))

	entities=[]
	for entity in response['entities']:
		entities.append(entity['text'].encode('utf-8'))
	
	time.sleep(10)
	response = api.keywords('text',text, { 'sentiment':1 })
	if  response['status']!='OK':
		raise Exception('Error from alchemy.\nText:%s\nStatus is:%s\nResponse:%s'%(text,response['status'],response))
	
	keywords=[]
	for keyword in response['keywords']:
		keywords.append(keyword['text'].encode('utf-8'))

	return entities,keywords

