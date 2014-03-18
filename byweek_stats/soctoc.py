from igraph import *
import numpy as np
import csv

'''
SET UP ENVIRONMENT:
mkdir /tmp/soclust/

cp /scratch/DSL/sincere-big-server/cnnfox/lemur-clusts-csv/lemur-cluster-10.clust.csv /tmp/soclust/
'''

POST_ID=0 #no-appendix 'p'
LEMUR_CLUST=1
def loadLemurClustFromFile(f_lemur_clust):
	
	lemur_clust={}
	with open(f_lemur_clust,'rb') as f:
		reader=csv.reader(f,delimiter="\t", quoting=csv.QUOTE_NONE)
		for row in [row for row in reader if row[0][0]!='#']:			
			lemur_clust['p'+row[POST_ID]]=int(row[LEMUR_CLUST])

	return lemur_clust

def loadLemurClustToGraph(g,lemur_clust,lemurXXprop='lemurXX'):
	for vdoc in [vdoc for vdoc in g.vs if vdoc['name'][0]=='p']:
		if vdoc['name'] in lemur_clust:
			vdoc[lemurXXprop]=lemur_clust[vdoc['name']]
		else:
			vdoc[lemurXXprop]=-1

