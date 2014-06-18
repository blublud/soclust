from igraph import *
import numpy as np
import csv

import sys; sys.path.append('/proj/DSL/sincere/big-server/_gited/');import csv_kv
import sys; sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/select_by_event');import by_event_io as eventIO
import sys; sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/byweek_stats/'); import textgraph
import sys; sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/byweek_stats/'); import byparallel
import sys; sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/select_by_event');import graph_with_properties

'''
ENVIRONMENT SETUP:
tar -xzvf /scratch/DSL/sincere-big-server/cnnfox/byweek/cnn_comment_yearweek.ncol.tar.gz -C /tmp/soclust/

'''
#f_ncol='/tmp/soclust/cnn_comment_yearweek.ncol'
f_ncol='/tmp/soclust/cnn2009_event_CommentLikes.ncol'

f_text='/tmp/soclust/cnn_text.csv'
#f_event='/scratch/DSL/sincere-big-server/cnnfox/select_by_event/cnn2009_postid_event.csv'
f_event='/tmp/soclust/cnn2009_postid_eventid.csv'
f_LIWC_Hierarchy='/tmp/soclust/liwc/cnn2009_liwcHierarchy.csv'
f_LIWC_KMeans='/tmp/soclust/liwc/cnn2009_liwcKMeans.csv'
f_lemur12='/tmp/soclust/lemur12.csv'

#f_output='/tmp/soclust/cnn2009_Comment_EventClustText.graphml'
f_output='/tmp/soclust/cnn2009_CommentLikes_EventClustTextLIWCLemur12_LeadEigen.graphml'

def main():

	g = get_graph_text_event_clust()
	g.write_graphml(f_output)

def get_graph_text_event_clust():
	
	texts=textgraph.loadTextFromFile(f_text)
	postid_eventids=csv_kv.load(f_event)

	g=Graph.Read_Ncol(f_ncol,directed=False)
	posts=postid_eventids.keys()
	vDocs=[v for v in g.vs if v['name'] in posts]
	
	###
	vs_s=g.neighborhood(vDocs,order=1)
	vs=set()
	for s in vs_s:
		vs=vs.union(s)
	sg=g.subgraph(vs,implementation='create_from_scratch')
	
#sg=sg.subgraph([v for v in sg.vs if v.degree()>1])
	###
	doCompoClustering(sg)
	graph_with_properties.loadPropertyToGraph(sg,texts,'message')
	graph_with_properties.loadPropertyToGraph(sg,postid_eventids,'event')
	
	liwc_h=graph_with_properties.loadPropertiesFromFile(f_LIWC_Hierarchy)
	liwc_k=graph_with_properties.loadPropertiesFromFile(f_LIWC_KMeans)
	lemur12=graph_with_properties.loadPropertiesFromFile(f_lemur12)

	graph_with_properties.loadPropertyToGraph(sg,liwc_k,'liwc_k')
	graph_with_properties.loadPropertyToGraph(sg,liwc_h,'liwc_h')
	graph_with_properties.loadPropertyToGraph(sg,lemur12,'lemur12')

	return sg

def doCompoClustering(g,compo_prop='compo',clust_prop='clust'):
	vertices={v['name']:v for v in g.vs}
	g.simplify()
	compos=g.components().subgraphs()
	for i,compo in enumerate(compos):
		for v in compo.vs:
			v[compo_prop]=i
		clusts=doClustering(compo)
		for j,vs in enumerate(clusts):
			for v in vs:
				vertices[v['name']][compo_prop]=str(int(i))
				vertices[v['name']][clust_prop]=str(int(j))


def doClustering(g):
	g.to_undirected()
	clusts=[]
	
#	for clust in g.community_fastgreedy().as_clustering().subgraphs():
	for clust in g.community_leading_eigenvector().subgraphs():
		
		clusts.append([v for v in clust.vs])	
		
	return clusts



if __name__ =='__main__':
	main()
	
