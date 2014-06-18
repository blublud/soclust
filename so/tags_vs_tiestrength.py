#!/bin/python
import MySQLdb
import igraph
from igraph import Graph

import sys;sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/igraph_extension')
from bipart import BiPart

import numpy as np
from sklearn import metrics

sql_getvotes='SELECT CONCAT("u",UserId),CONCAT("p",PostId) FROM votes WHERE PostId IN (SELECT Id FROM posts WHERE DATE(CreationDate)="2012-12-20" AND Tags IS NOT NULL);'

def __main__():
	db=MySQLdb.connect(host='localhost',user='root',passwd='toor',db='so')
	cur=db.cursor()
	cur.execute(sql_getvotes)
	edges=[(row[0],row[1]) for row in cur.fetchall()] #row[0]=user;row[1]=post
	g=BiPart.TupleList(edges,directed=False)
	#load tags to post vertices, remove those have no tag
	for v in [v for v in g.vs if v['name'][0]=='p']:
		temp=cur.execute('SELECT Tags FROM posts WHERE Id=%s'%v['name'][1:])
		tags=cur.fetchone()
		if tags is None:
			v.delete()
		else:
			v['tags']=tags[0]
	#find the proxy tag in the level from 0 to max_level
	tags_hierarchy=loadTagHierarchyList('/tmp/so/tag_hierachy2012.graphml')
	max_level=max([len(ancestors) for _,ancestors in tags_hierarchy.items()])
	for v in [v for v in g.vs if v['name'][0]=='p']:
		tags=v['tags']
		tags=('>'+tags+'<').split('><')[1:-1]
		for l in range(max_level):
			proxytag=getTagProxyCompound(tags_hierarchy,tags,l)
			if (proxytag): 
				v['tag_%d'%l]=proxytag
			else:
				break#should we remove v has no tag in tag tree? this won't happen b/c there's always __root__ node
	#do kmeans tiestrength clustering:
	
	max_tag_max_level=len(set([v['tag_%d'%(max_level-1)] for v in g.vs if v['name'][0]=='p']))
	cluster_counts=[1]
	while (cluster_counts[-1]*2 <= max_tag_max_level):
		cluster_counts.append(cluster_counts[-1]*2)
	for cc in cluster_counts:
		g.cluster_tiestrength_kmeans(vertices=[v for v in g.vs if v['name'][0]=='p'],nclusters=cc,cluster_prop='tsk_%d'%cc)

	#check with lemur
	for cc in cluster_counts:
		g.loadPropsFromFile('/tmp/so/posts20Dec2012_lemur%d.lemur'%cc, 'lemur_%d'%cc)

	#evaluation 
	cluster_evals=np.zeros((max_level,len(cluster_counts)))#for each tag_level, measure tie-strength clustering performance
	cluster_evals=[]
	proxytag_atlevels={}
	vs=[v for v in g.vs if v['name'][0]=='p']
	for tag_level in range(max_level):
		proxytag_atlevels[tag_level]=len(set([v['tag_%d'%tag_level] for v in vs]))
		clusteval_taglevel=[]
		for i,cluster_count in enumerate(cluster_counts):
			clust_vs_tag=g.clustereval_weightedsumentropy(vs,'tag_%d'%tag_level,'tsk_%d'%cluster_count)
			lemur_vs_tag=g.clustereval_weightedsumentropy(vs,'tag_%d'%tag_level,'lemur_%d'%cluster_count)
			clusteval_taglevel.append((clust_vs_tag,lemur_vs_tag))
		cluster_evals.append(clusteval_taglevel)

	print 'break here'


def loadTagHierarchyList(f_taghierachy):
	tagtree=Graph.Read_GraphML(f_taghierachy)
	tags={}
	#tags={tag:[ancestor0,ancestor1]}
	for v in [v for v in tagtree.vs if v.degree()>0]:
		tag=v['name'][1:]
		parents=[]
		while(True):
			neighbors=v.neighbors(mode=igraph.OUT)
			if len(neighbors):
				parent=neighbors[0]
				parents.insert(0,parent['name'][1:])
				v=parent
			else:
				break
		tags[tag]=parents.insert(0,'__root__')
		parents.append(tag)
		tags[tag]=parents
	return tags

def getTagProxy(tags_hierarchy,realtag,level):
	ancestor_tags=tags_hierarchy[realtag]
	if level > len(ancestor_tags):
		return ancestor_tags[-1]
	else:
		return ancestor_tags[level]

def getTagProxyCompound(tags_hierarchy,realtags,level):
	tags_ancestors=[tags_hierarchy[t] for t in realtags if t in tags_hierarchy]
	if len(tags_ancestors)==0:
		return None
	searched_level=min(level+1, max([len(ans)for ans in tags_ancestors]))
	proxytag=None
	for l in range(searched_level):
		tags_at_level=[t for t in [ans[l] for ans in tags_ancestors if len(ans) > l]]
		if len(set(tags_at_level))==1:
			proxytag=tags_at_level[0]
		else:
			break
	return proxytag


if __name__=='__main__':
	__main__()


