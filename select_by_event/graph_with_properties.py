from igraph import *
import csv

def doCompoClustering(g,compo_prop='compo',clust_prop='clust'):
	vertices={v['name']:v for v in g.vs}
	g.simplify()
	compos=g.components().subgraphs()
	for i,compo in enumerate(compos):
		for v in compo.vs:
			v[compo_prop]=i
		clusts=byparallel.doClustering(compo)
		for j,vs in enumerate(clusts):
			for v in vs:
				vertices[v['name']][compo_prop]=i
				vertices[v['name']][clust_prop]=j


def loadPropertyToGraph(g,vertex_propVals,propName,id_prop='name'):

	for v in g.vs:
		vid=v[id_prop] 
		if vid in vertex_propVals:
			v[propName]= vertex_propVals[vid]


			
def loadPropertiesFromFile(f_csv,delim='\t'):
	with open(f_csv) as f:
		reader=csv.DictReader(f,['vertexId','propVal'],delimiter=delim)
		props={}
		for r in reader:
			props[r['vertexId']]=r['propVal']

	return props
