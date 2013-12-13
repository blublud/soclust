'''
Calculate standard deviations of several social clustering configuration (# of clusters) using igraph
+Reads all clustering results (stored in /scratch/DSL/sincere-big-server/cnnfox/soclust-igraph/)
+Calculate standard deviation of that clustering result.
+Put in a dict {cluster-count -> std deviation}
+Output the dict to a csvfile
'''
#!/bin/python
import numpy
import os
import sys

sys.path.append('/proj/DSL/sincere/big-server/cnnfox/')
import soctoc

dr='/scratch/DSL/sincere-big-server/cnnfox/soclust-igraph/'
h_std={}
for f in os.listdir(dr):
	print f
	g=soctoc.dictbygroup(soctoc.loadcsv(dr+f))	
	stdev=numpy.std([len(v) for k,v in g.items()])	
	clustcount=f.split('-')[1]
	h_std[clustcount]=stdev

soctoc.savecsv(h_std,'/scratch/DSL/sincere-big-server/cnnfox/soclust-std.csv')
