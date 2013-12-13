from igraph import *
import cPickle
import os
import numpy as np
import time
from random import choice

def get_cowatch_min_edges(build_for='p'):

	g=Graph.Read_Ncol('/tmp/cnn-comp0.csv')
	g.to_undirected()

	# g2 is g^2
	g2=g.copy()
	g2.delete_edges(g2.es)
	nwEdges=[]

	vs=getall_vertices(g,build_for)
	seeds=choice(vs)
	print "# of seeds is:%d"%len(seeds)
	vs=seeds
	
	for v1 in vs:
		tmpEdges=[]
		min_proximity=0
		degree1=v1.degree()
		nb1=set(g.neighborhood(v1.index))
		for v2 in [g.vs[v] for v in g.neighborhood(v1.index,order=2) if is_vertextype(g.vs[v],build_for) and v > v1.index]:
			degree2=v2.degree()
			co_watch=nb1 & set(g.neighborhood(v2.index))
			co_watch=float(len(co_watch))
			co_watch=(co_watch/degree1 + co_watch/degree2)
			if co_watch==min_proximity:
				tmpEdges.append((v1.index,v2.index))
			elif co_watch > min_proximity:
				tmpEdges=[(v1.index,v2.index)]
		
		nwEdges.append(tmpEdges)
	
	f=open('/tmp/cowatch_min_edges.csv','w')
	for (v1,v2) in nwEdges:
		write(f,"%s\t%s\n"%(v1,v2))
	f.close()
	return nwEdges

def is_vertextype(v, typ):
	return v['name'][0]==typ

def getall_vertices(g, typ):
	return [v for v in g.vs if is_vertextype(v, typ)]

if __name__ == '__main__':	
	get_cowatch_min_edges()
