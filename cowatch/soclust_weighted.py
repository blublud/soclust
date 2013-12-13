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
'''
NOTE:
0.08 ==> 0 new edges
0.01 ==> 0 new edges
total % 0.01 ==> 0
total 0.001 ==>
'''
g=Graph.Read_Ncol('/tmp/cnn.csv')
g.to_undirected()

# g2 is g^2
g2=g.copy()
g2.delete_edges(g2.es)
nwEdges=[]

docvs = [v for v in g.vs if v['name'][0]=='p']
for d1 in docvs:
	degree1=d1.degree()
	nb1=set(g.neighborhood(d1.index))
	tmpEdges={}
	for d2 in [g.vs[v] for v in g.neighborhood(d1.index,order=2) if g.vs[v]['name'][0]=='p' and v > d1.index]:
		degree2=d2.degree()
		co_watch=nb1 & set(g.neighborhood(d2.index))
		co_watch=float(len(co_watch))
		co_watch=(co_watch/degree1 + co_watch/degree2)
		tmpEdges[(d1.index,d2.index)]=co_watch
		if co_watch > 0.3:
			nwEdges.append((d1.index,d2.index))

g2.add_edges(nwEdges)
gdoc=g2.induced_subgraph(docvs)
g2.write_ncol('/tmp/cnn2doc-0-08.csv')
os.system("/proj/DSL/sincere/big-server/scriptlib/backup.sh /tmp/cnn2doc-0-08.csv /scratch/DSL/sincere-big-server/cnnfox/co-watcher/ cnn2doc-0-08.csv")

gdoc.to_undirected()
dendogram=gdoc.community_fastgreedy()
cPickle.dump(dendogram,open('/tmp/cnn2doc-008-dendo.dat', 'w'))
os.system("/proj/DSL/sincere/big-server/scriptlib/copy-retry.sh /tmp/cnn2doc-008-dendo.dat /scratch/DSL/sincere-big-server/cnnfox/co-watcher/")
