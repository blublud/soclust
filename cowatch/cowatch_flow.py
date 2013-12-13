from igraph import *
import cPickle
import os
import numpy as np
import time
import random

def build_cowatch_flow(g,srcV,length=100):

	vs=[srcV.index]
	cowatches=[1.0]
	while(len(vs) < length):
		v=vs[-1]
		(nextV,cowatch)=get_nextV(g,g.vs[v])
		print 'step',len(vs),'id',nextV.index,'neighbors:',len(nextV.neighbors()), 'cowatch',cowatch
		if nextV is None or nextV.index in vs: break
		vs.append(nextV.index)
		cowatches.append(cowatch)
	
	return (vs,cowatches)		


def get_nextV(g, vertex):

	v1=vertex
	vtype=v1['name'][0]	
	nb1=set(g.neighborhood(v1.index))
	min_proximity=0
	nextV=None
	for v2 in [g.vs[vid] for vid in g.neighborhood(v1.index, order=2) if vid != v1.index and g.vs[vid]['name'][0]==vtype]:
		co_watch=nb1 & set(g.neighborhood(v2.index))
		co_watch=float(len(co_watch))
		co_watch=(co_watch/v1.degree())		
		if co_watch > min_proximity:
			nextV=v2
			min_proximity=co_watch
	
	return (nextV, min_proximity)

if __name__ == '__main__':
	g=Graph.Read_Ncol('/tmp/cnn.csv')
	g.to_undirected()
	srcV=random.choice([v for v in g.vs if v['name'][0]=='p'])
	(vs,cws)=build_cowatch_flow(g,srcV,length=10)
	print [len(v.neighbors()) for v in vs]
	print cws
