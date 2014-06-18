import os

import sys;sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/igraph_extension')
from bipart import BiPart

f_ncol='/tmp/nyt/ncol.ncol'
f_postid_soclust='/tmp/nyt/postid_soclust.csv'
f_graphml='/tmp/nyt/graphml.graphml'
f_post_message='/tmp/nyt/postid_message.csv'
f_postid_lemur='/tmp/nyt/postid_lemur.csv'
f_postid_eventid='/tmp/nyt/postid_eventid.csv'
n_cluster=15

#do soclust
g=BiPart.Read_Ncol(f_ncol)
g.cluster_tiestrength_kmeans(vertices=[v for v in g.vs if v['name'][0]=='p'],nclusters=n_cluster,cluster_prop='tsk_%d'%n_cluster)

#do lemur
os.system('python /proj/DSL/sincere/big-server/_gited/soclust/lemur_clust/lemur_clustering.py %s %s %d'%(f_post_message,f_postid_lemur,n_cluster))
g.loadPropsFromFile(f_postid_lemur,propName='lemur_%d'%n_cluster)

#event - ground truth
g.loadPropsFromFile(f_postid_eventid,propName='event')

#do compare
vs=[v for v in g.vs if v['name'][0]=='p']
clust_vs_event=g.clustereval_weightedsumentropy(vs,'event','tsk_%d'%n_cluster)
lemur_vs_event=g.clustereval_weightedsumentropy(vs,'event','lemur_%d'%n_cluster)

print 'Weighted Sum Entropy'
print 'clust_vs_event',clust_vs_event
print 'lemur_vs_event',lemur_vs_event

clust_vs_event=g.clustereval_adjustedRand(vs,'event','tsk_%d'%n_cluster)
lemur_vs_event=g.clustereval_adjustedRand(vs,'event','lemur_%d'%n_cluster)
print 'Adjust Rand Index'
print 'clust_vs_event',clust_vs_event
print 'lemur_vs_event',lemur_vs_event

clust_vs_event=g.clustereval_mutualinfo(vs,'event','tsk_%d'%n_cluster)
lemur_vs_event=g.clustereval_mutualinfo(vs,'event','lemur_%d'%n_cluster)
print 'Ajusted Mutual Information'
print 'clust_vs_event',clust_vs_event
print 'lemur_vs_event',lemur_vs_event

