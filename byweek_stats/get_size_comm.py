from igraph import *
import numpy as np
import csv
from concurrent import futures

'''
setup environment
wget http://mirrors.kernel.org/ubuntu/pool/universe/p/python-concurrent.futures/python-concurrent.futures_2.1.2-1_all.deb
sudo apt-get install python-suppor
sudo dpkg -i python-concurrent.futures_2.1.2-1_all.deb
'''

f_ncol='/tmp/cnn_comment_yearweek.ncol'
f_stats='/tmp/byweek_stats/%05d_cnn_byweek_stats.csv'
f_cluster_result='/tmp/byweek_clusts/%05d_weekclust.csv'

def main():

	g= Graph.Read_Ncol(f_ncol,directed=False)

	weeks={int(e['weight']) for e in g.es}
	minweek=min(weeks)
	maxweek=max(weeks)
	
	args=((g,week) for week in range(minweek,maxweek+1))

	for week in range(minweek,maxweek+1):
		getStats((g,week))

def getStats(arg):
	try:
		(g, week)=arg	
		es=[e for e in g.es if e['weight']==week]
		sg=g.subgraph_edges(es)	
		componentCount=len(sg.components().subgraphs())

		clusts=doClustering(sg)	
		saveClusteringResult(f_cluster_result%week,clusts)

		clustCount=len(clusts)
		clustSizes=[len(c)for c in clusts]
		clustSizeMean=np.mean(clustSizes)
		clustSizeStd=np.std(clustSizes)

		with open(f_stats%week,'wb') as fcsv:
			writer=csv.writer(fcsv,delimiter="\t")
			writer.writerow([week, sg.vcount(),sg.ecount(),componentCount,clustCount,clustSizeMean,clustSizeStd])
	except Exception as e:
		print 'error at %d'%week, str(e)	

def doClustering(g):
	g.to_undirected()
	clusts=[]
	
	for clust in g.community_fastgreedy().as_clustering().subgraphs():
		clusts.append(clust.vs)

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
				writer.writerow([i,v['name']])

if __name__ == '__main__':
	main()
		
