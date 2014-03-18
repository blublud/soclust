from igraph import *
import numpy as np
import csv
from concurrent import futures
#from .. import soctoc_entropy as ste
import sys; sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/');import soctoc_entropy as ste
import sys; sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/byweek_stats/'); import byparallel
#import sys; sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/');import soctoc_entropy as ste

'''
SET UP ENVIRONMENT:
mkdir /tmp/soclust/
mkdir /tmp/soclust/weekgraph/
mkdir /tmp/soclust/wordcloud/
tar -xzvf /scratch/DSL/sincere-big-server/cnnfox/byweek/cnn_comment_yearweek.ncol.tar.gz -C /tmp/soclust/
tar -xzvf /scratch/DSL/sincere-big-server/cnnfox/byweek/entropy_drop/cnn_dropentropy_message.csv.tar.gz -C /tmp/soclust/
wget http://mirrors.kernel.org/ubuntu/pool/universe/p/python-concurrent.futures/python-concurrent.futures_2.1.2-1_all.deb
sudo apt-get install python-support
sudo dpkg -i python-concurrent.futures_2.1.2-1_all.deb

cp /proj/DSL/sincere/big-server/_gited/soclust/byweek_stats/api_key.txt /tmp/soclust/
cd /tmp/soclust/

AlchemyAPI key:
c016268f5e5d1f1ea96e74c46be91719c4ce4c8c

'''
import logging
import textgraph
import sys; sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/byweek_stats/'); import textgraph
import sys; sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/byweek_stats/'); import byparallel
import sys; sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/byweek_stats/'); import soctoc

#drop_entropy_weeks=['200909', '200910', '200912', '200915', '200916', '200921', '200922', '200924', '200925', '200930', '200934', '200941', '200948', '201001', '201002', '201012', '201013', '201015', '201038', '201042', '201202', '201203', '201216', '201243', '201244', '201245', '201246', '201247', '201301', '201303', '201304']
drop_entropy_weeks=['200924', '200925', '200930', '200934', '200941', '200948', '201001', '201002', '201012', '201013', '201015', '201038', '201042', '201202', '201203', '201216', '201243', '201244', '201245', '201246', '201247', '201301', '201303', '201304']

f_ncol='/tmp/soclust/cnn_comment_yearweek.ncol'
f_weekgraph='/tmp/soclust/weekgraph/%d.graphml'
f_texts='/tmp/soclust/cnn_dropentropy_message.csv'
f_wordCloud='/tmp/soclust/wordClouds.csv'
f_lemur10='/tmp/soclust/lemur-cluster-10.clust.csv'

g = Graph()

def main():

#lemur_only
	doAllLemurClust()#does not work:cannot add more attributes to graph loaded from graphml.

'''
	g= Graph.Read_Ncol(f_ncol,directed=False)
	
	texts=textgraph.loadTextFromFile(f_texts)
	
	weeks=[float(w) for w in drop_entropy_weeks]
	texts=textgraph.loadTextFromFile(f_texts)
	wordClouds=textgraph.getWordClouds(texts)

	args=((g,week,texts,wordClouds) for week in weeks)

	for arg in args:
		doAll(arg)

	arg=(g,201245.0,texts)
	doAll(arg)

#lemur_only
	doAllLemurClust()#does not work:cannot add more attributes to graph loaded from graphml.

#parallel
	with futures.ThreadPoolExecutor(max_workers=64) as executor:
		for i in executor.map(doAll, args):
			pass

'''

def doAllLemurClust():
	lemur_clust=soctoc.loadLemurClustFromFile(f_lemur10)
	weeks=[int(w) for w in drop_entropy_weeks]
	args=((week,lemur_clust) for week in weeks)
	for arg in args:
		lemurClust(arg)

	
def lemurClust(arg):
	(week,lemur_clust)=arg
	try:
		gweek=Graph.Read_GraphML(f_weekgraph%week)
		gweek=gweek.copy()#??
		soctoc.loadLemurClustToGraph(gweek,lemur_clust,lemurXXprop='lemur10')
		f=open(f_weekgraph%week,'w')
		gweek.write_graphml(f)
		f.close()
	except Exception, err:
		sys.stderr.write('Error at week %d.Details:%s'%(int(week),str(err)))
		raise err
	
def wordCloud():
	texts=textgraph.loadTextFromFile(f_texts)
	wordClouds=textgraph.getWordClouds(texts)
	textgraph.saveWordClouds(wordClouds,f_wordCloud)

def doAll(arg):
	(g, week,texts,lemur_clust)=arg	
	
	try:
		gweek=getGraphOWeek(g,week)
		textgraph.loadTextToGraph(gweek,texts)
		soctoc.loadLemurClustToGraph(gweek,lemur_clust,lemurXXprop='lemur10')
		doCompoClustering(gweek)
		f=open(f_weekgraph%week,'w')
		gweek.write_graphml(f)
		f.close()
	except Exception, err:
		sys.stderr.write('Error at week %d.Details:%s'%(int(week),str(err)))
		raise err


def doCompoClustering(g,compo_prop='compo',clust_prop='clust'):
	vertices={v['name']:v for v in g.vs}
	g.simplify()
	compos=g.components().subgraphs()
	for i,compo in enumerate(compos):
		for v in compo.vs:
			v[compo_prop]=i
		clusts=byparallel.doClustering(compo)
		for j,vs in enumerate(clusts):
			for v in vs:
				vertices[v['name']][compo_prop]=i
				vertices[v['name']][clust_prop]=j


def getGraphOWeek(g,week):
	
	es=[e for e in g.es if e['weight']==week]
	if len(es)==0: return
	g=g.subgraph_edges(es)
	g.simplify()
	return g

if __name__ == '__main__':
	main()
