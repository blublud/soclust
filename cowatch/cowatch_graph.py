from igraph import *
import cPickle
import os
import numpy as np
import time
'''
#CNN-comment.csv: list of edges for this graph
#vertex name has format: [u|d]-<id>
#	id:fbid of document(post) or user
	u:signify that this fbid refers to a user
	d:signifiy that this fbid refers to a document
'''

def build_cowatch_graph(min_cowatch_percent=0.3, build_for='p'):

	g=Graph.Read_Ncol('/tmp/cnn.csv')
	g.to_undirected()

	# g2 is g^2
	g2=g.copy()
	g2.delete_edges(g2.es)
	nwEdges=[]

	vs = getall_vertices(g,build_for)
	
	for v1 in vs:
		degree1=v1.degree()
		nb1=set(g.neighborhood(v1.index))
		for v2 in [g.vs[v] for v in g.neighborhood(v1.index,order=2) if is_vertextype(g.vs[v],build_for) and v > v1.index]:
			degree2=v2.degree()
			co_watch=nb1 & set(g.neighborhood(v2.index))
			co_watch=float(len(co_watch))
			co_watch=0.5*(co_watch/degree1 + co_watch/degree2)
			if co_watch > min_cowatch_percent:
				nwEdges.append((v1.index,v2.index))

	g2.add_edges(nwEdges)
	g_induced=g2.induced_subgraph(vs)
	ncol_fname="/tmp/cnn2-%s-%f.csv"%(build_for,min_cowatch_percent)
	g_induced.write_ncol(ncol_fname)
	os.system("/proj/DSL/sincere/big-server/scriptlib/backup.sh %s /scratch/DSL/sincere-big-server/cnnfox/co-watcher/ %s"%(ncol_fname,ncol_fname.split('/')[-1]) )

	g_induced.to_undirected()
	dendogram=g_induced.community_fastgreedy()
	dendo_fname='/tmp/cnn2-dendo-%s-%f.dat'%(build_for,min_cowatch_percent)
	cPickle.dump(dendogram,open(dendo_fname, 'w'))
	os.system("/proj/DSL/sincere/big-server/scriptlib/copy-retry.sh %s /scratch/DSL/sincere-big-server/cnnfox/co-watcher/"%dendo_fname)

def is_vertextype(v, typ):
	return v['name'][0]==typ

def getall_vertices(g, typ):
	return [v for v in g.vs if is_vertextype(v, typ)]


def do_clustering(dendroFile='/tmp/cnn2-dendo-p-0.700000.dat', resultfile='/mnt/large/co-watch/clusters/'):

	dendogram=cPickle.load(open(dendroFile,'r'))

	clust=dendogram.as_clustering()	
	f=open(resultfile,'w')	
	for i,subg in enumerate(clust.subgraphs()):
		for v in subg.vs:
			f.write(v['name']+"\t"+str(i)+"\n")
	f.close()

	os.system("/proj/DSL/sincere/big-server/scriptlib/copy-retry.sh %s /scratch/DSL/sincere-big-server/cnnfox/cowatch %s"%(resultfile) )


def get_dendrogram(g, fname=None):
	dendogram=g.community_fastgreedy()
	if fname:
		cPickle.dump(dendogram,open(fname, 'w'))
	return dendogram


if __name__ == '__main__':
	build_cowatch_graph(min_cowatch_percent=0.5, build_for='p')
	
	#get dendrogram:
	#g05=Graph.Read_Ncol('/tmp/cnn-0_5-comp0.csv')
	#g05.to_undirected()
	#dd=get_dendrogram(g07,'/tmp/cnn-0_5-comp0-dendro.dat')

	#do clustering:
	#dd=cPickle.load(open('/tmp/cnn^2-p-50-dendro.dat','r'))
	#do_clustering(dd,[None],result_dir='/tmp/co-watch/cnn-0_08_clusters/')

