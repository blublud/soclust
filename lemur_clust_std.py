#!/bin/python
import numpy
import os
import sys

sys.path.append('/proj/DSL/sincere/big-server/cnnfox/')
import soctoc

dr='/scratch/DSL/sincere-big-server/cnnfox/lemur-clusts-freq/'
h_std={}
for f in os.listdir(dr):
	clustcount=f.replace('.','-').split('-')[2]	
	stdev=numpy.std([int(v) for v in soctoc.loadcsv(dr+f).values()])
	h_std[clustcount]=stdev

soctoc.savecsv(h_std,'/scratch/DSL/sincere-big-server/cnnfox/lemur-clust-std.csv')
