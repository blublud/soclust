from igraph import *
import csv
from concurrent import futures

f_input_ncol='/tmp/socgraph/cnn_comment_yearweek.ncol'
f_output_graphml='/tmp/socgraph/output/week%d.graphml'

'''
This snippet:
	+reads in a "big-graph" in which edges are created at different time (different weeks).
	+Partitions "big-graph" into smaller subgraphs by weeks
	+For each subgraph, finds the components and clusters in each components
the input is f_input_ncol (in ncol format)
the output,each subgraph for one week is stored in one file (graphml format)

'''

def main():

	#read input(social graph, edge's weight is interpreted as the week in which the edge is created)
	g= Graph.Read_Ncol(f_input_ncol,directed=False)

	weeks={int(e['weight']) for e in g.es}
	minweek=min(weeks)
	maxweek=max(weeks)

	args=((g,week) for week in range(minweek,maxweek+1))
	with futures.ThreadPoolExecutor(max_workers=64) as executor:
		for i in executor.map(worker_clustering, args):
			pass

def worker_clustering(arg):

	(g, week)=arg	

	es=[e for e in g.es if e['weight']==week]
	if len(es)==0: return
	g=g.subgraph_edges(es)
	g.simplify()
	doCompoClustering(g)
	g.write_graphml(f_output_graphml%int(week))


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
				vertices[v['name']][compo_prop]=i
				vertices[v['name']][clust_prop]=j

def doClustering(g):
	g.to_undirected()
	clusts=[]
	
	for clust in g.community_fastgreedy().as_clustering().subgraphs():
		clusts.append([v for v in clust.vs])

	return clusts

if __name__=='__main__':
	main()
