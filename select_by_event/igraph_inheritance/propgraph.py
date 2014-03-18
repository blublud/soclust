from igraph import *
import csv
class PropGraph(Graph):

	def loadProperties(self, vertex_propVals,propName,id_prop='name'):
		
		for v in self.vs:
			vid=v[id_prop] 
			if vid in vertex_propVals:
				v[propName]= vertex_propVals[vid]

	def loadPropsFromFile(self, fProp, propName,id_prop='name',delim='\t'):
		
		with open(fProp) as f:
			reader=csv.DictReader(f,['vertexId','propVal'],delimiter=delim)
			props={}
			for r in reader:
				props[r['vertexId']]=r['propVal']
		
		self.loadProperties(props,propName,id_prop)