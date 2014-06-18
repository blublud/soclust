from igraph import *
import csv

def loadProperties(graph, vertex_propVals,propName,id_prop='name'):
	for v in graph.vs:
		vid=v[id_prop] 
		if vid in vertex_propVals:
			v[propName]= vertex_propVals[vid]

def loadPropsFromFile(graph, fProp, propName,id_prop='name',delim='\t'):
	with open(fProp) as f:
		reader=csv.DictReader(f,['vertexId','propVal'],delimiter=delim)
		props={}
		for r in reader:
			props[r['vertexId']]=r['propVal']
	
	loadProperties(graph,props,propName,id_prop)

