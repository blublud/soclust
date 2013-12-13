from igraph import *
import numpy as np
import csv
from concurrent import futures
#from .. import soctoc_entropy as ste
import sys; sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/');import soctoc_entropy as ste
#import sys; sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/');import soctoc_entropy as ste

'''
SET UP ENVIRONMENT:
mkdir -p /mnt/large/entropy_drop/weekgraph/
tar -xzvf /scratch/DSL/sincere-big-server/cnnfox/byweek/cnn_comment_yearweek.ncol.tar.gz -C /tmp/

wget http://mirrors.kernel.org/ubuntu/pool/universe/p/python-concurrent.futures/python-concurrent.futures_2.1.2-1_all.deb
sudo apt-get install python-support
sudo dpkg -i python-concurrent.futures_2.1.2-1_all.deb

'''
import logging

drop_entropy_weeks=['200934', '200930', '201203', '201202', '200922', '200921', '200925', '200924', '201042', '201038', '200948', '200941', '201245', '201012', '201013', '201015', '201243', '201002', '201001', '201304', '201247', '201246', '201301', '200912', '200910', '200916', '200915', '201244', '201303', '200909', '201216']

f_ncol='/tmp/cnn_comment_yearweek.ncol'
f_weekgraph='/mnt/large/entropy_drop/weekgraph/%d.graphml'

g = Graph()

def main():

	g= Graph.Read_Ncol(f_ncol,directed=False)
	
	weeks=[float(w) for w in drop_entropy_weeks]
	
	args=((g,week) for week in weeks)
	with futures.ThreadPoolExecutor(max_workers=64) as executor:
		for i in executor.map(getByWeekGraphs, args):
			pass

'''
	getByWeekGraphs((g,200934.0))

'''

def getByWeekGraphs(arg):
	(g, week)=arg	

	es=[e for e in g.es if e['weight']==week]
	if len(es)==0: return
	g=g.subgraph_edges(es)
	g.simplify()
	f=open(f_weekgraph%week,'w')
	g.write_graphml(f)
	f.close()

	
'''
Get the very details of a graph:
	+for each component in graph:
		+Plot
		+Word cloud
		+For each cluster in component:
			+Plot
			+Word cloud
			+Get content, its lemur cluster,
'''

if __name__ == '__main__':
	main()
