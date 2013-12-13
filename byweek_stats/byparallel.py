from igraph import *
import numpy as np
import csv
from concurrent import futures
#from .. import soctoc_entropy as ste
import sys; sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/');import soctoc_entropy as ste
#import sys; sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/');import soctoc_entropy as ste

import logging

lgr=logging.getLogger('logger')
ch=logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
lgr.addHandler(ch)

'''
setup environment

rm -r /tmp/byweek_stats/
rm -r /tmp/byweek_clusts/
mkdir /tmp/byweek_stats/
mkdir /tmp/byweek_clusts/

mkdir /tmp/lemur_clusts/
cp /scratch/DSL/sincere-big-server/cnnfox/byweek/cnn_comment_yearweek.ncol.tar.gz /tmp/
tar -xzvf /tmp/cnn_comment_yearweek.ncol.tar.gz -C /tmp/


wget http://mirrors.kernel.org/ubuntu/pool/universe/p/python-concurrent.futures/python-concurrent.futures_2.1.2-1_all.deb
sudo apt-get install python-support
sudo dpkg -i python-concurrent.futures_2.1.2-1_all.deb
'''
f_ncol='/tmp/cnn_comment_yearweek.ncol'
f_stats='/tmp/byweek_stats/%05d_cnn_byweek_stats.csv'
f_cluster_result='/tmp/byweek_clusts/%05d_weekclust.csv'

lemur_class_dir='/scratch/DSL/sincere-big-server/cnnfox/lemur-clusts-csv/'
lemur_classified={'lemur-cluster-10.clust.csv':0,
					'lemur-cluster-20.clust.csv':0,
					'lemur-cluster-35.clust.csv':0,
					'lemur-cluster-100.clust.csv':0,
					'lemur-cluster-200.clust.csv':0,
					'lemur-cluster-500.clust.csv':0,
					'lemur-cluster-700.clust.csv':0,
					'lemur-cluster-1000.clust.csv':0}

stats_properties=[
	'week',
	'type',
	'seq',
	'vCount',
	'eCount',
	'docCount',
	'usrCount',
	'usrPerdoc',
	'degMean',
	'degStd',
	'usrDegMean',
	'usrDegStd',
	'docDegMean',
	'docDegStd',
	'diam',
	'entropy_absence',
	'lemur-cluster-10.clust.csv',
	'lemur-cluster-20.clust.csv',
	'lemur-cluster-35.clust.csv',
	'lemur-cluster-100.clust.csv',
	'lemur-cluster-200.clust.csv',
	'lemur-cluster-500.clust.csv',
	'lemur-cluster-700.clust.csv',
	'lemur-cluster-1000.clust.csv'
]


def main():

	g= Graph.Read_Ncol(f_ncol,directed=False)
	
	for fname in lemur_classified:
		lemur_classified[fname]=ste.loadcsv(lemur_class_dir+fname)

	weeks={int(e['weight']) for e in g.es}
	minweek=min(weeks)
	maxweek=max(weeks)

	#write header csv equal week 000
	with open(f_stats%0,'wb') as fcsv:
		writer=csv.writer(fcsv,delimiter="\t")
		seq=map(str.__add__,['#']*len(stats_properties),[str(i) for i in range(1,len(stats_properties)+1)]) 
		writer.writerow(map(str.__add__,seq,stats_properties))

	
	args=((g,week) for week in range(minweek,maxweek+1))
	with futures.ThreadPoolExecutor(max_workers=64) as executor:
		for i in executor.map(getStats, args):
			pass
'''

	arg=(g,200843)
	getStats(arg)
'''

def getStats(arg):

	(g, week)=arg	
	try:
		lgr.debug('Getting stats for week %d'%week)
		es=[e for e in g.es if e['weight']==week]
		if len(es)==0: return
		g=g.subgraph_edges(es)
		g.simplify()
		compos=g.components().subgraphs()
		stats_all=[]
		for i,sg in enumerate(compos):
			stats= getStatsByVertices(sg)
			stats['week']=week
			stats['type']='compo'
			stats['seq']=i
			
			stats_all.append(stats)
		
		#clusts=ste.dictbygroup(loadcsv(f_cluster_result%week))
		clusts=doClustering(g)	
		saveClusteringResult(f_cluster_result%week,clusts)		
		for i,vs in enumerate(clusts):
			stats= getStatsByVertices(g,vs)
			stats['week']=week
			stats['type']='clust'
			stats['seq']=i
			
			stats_all.append(stats)
		
		with open(f_stats%week,'wb') as fcsv:
			writer=csv.writer(fcsv,delimiter="\t")
			for stats in stats_all:
				values=[stats[k] for k in stats_properties]
				writer.writerow(values)
		lgr.debug('Getting stats for week %d: DONE'%week)
	except Exception:
		lgr.exception('error at %d'%week)


def getStatsByVertices(g, vertices=None):
	
	if vertices:
		g=g.induced_subgraph(vertices,implementation='create_from_scratch')
	
	#components=g.components().subgraphs()
	docs=[v for v in g.vs if v['name'][0]=='p']
	usrs=[v for v in g.vs if v['name'][0]=='u']
	
	vCount=g.vcount()
	eCount=g.ecount()
	docCount=len(docs)
	usrCount=len(usrs)
	usrPerdoc=-1; 
	if docCount: usrPerdoc=usrCount/docCount

	degMean=np.mean(g.degree(g.vs))
	degStd=np.std(g.degree(g.vs))

	docDegMean=np.mean(g.degree(docs))
	docDegStd=np.std(g.degree(docs))
	
	usrDegMean=np.mean(g.degree(usrs))
	usrDegStd=np.std(g.degree(usrs))

	diam=g.diameter(directed=False,unconn=True)

	docNames=[d['name'][1:] for d in docs]
	entropies={}

	for name,classified in lemur_classified.items():
		entropy=ste.getentropy(docNames,classified)
		entropies[name]=entropy
	entropy_absence=-1
	if len(lemur_classified):
		lemur_items=lemur_classified.values()[0]
		entropy_absence=len([i for i in docNames if i not in lemur_items])

	stats={
		'vCount':vCount,
		'eCount':eCount,
		'docCount':docCount,
		'usrCount':usrCount,
		'usrPerdoc':usrPerdoc,
		'degMean':degMean,
		'degStd':degStd,
		'usrDegMean':usrDegMean,
		'usrDegStd':usrDegStd,
		'docDegMean':docDegMean,
		'docDegStd':docDegStd,
		'diam':diam,
		'entropy_absence':entropy_absence
	}

	for name,entropy in entropies.items():
		stats[name]=entropy

	return stats

def doClustering(g):
	g.to_undirected()
	clusts=[]
	
	for clust in g.community_fastgreedy().as_clustering().subgraphs():
		clusts.append([v for v in clust.vs])

	return clusts

'''
input clusts is a list of lists:
	clusts=[vs1=[...], vs2=[...],... ]
'''
def saveClusteringResult(fname, clusts):
	with open(fname,'wb') as fcsv:
		writer=csv.writer(fcsv,delimiter="\t")
		for i,clust in enumerate(clusts):
			for v in clust:
				writer.writerow([v['name'],i])

if __name__ == '__main__':
	main()
		
