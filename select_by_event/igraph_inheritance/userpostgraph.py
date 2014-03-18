import sys
sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/select_by_event/igraph_inheritance')
from propgraph import PropGraph
from bipart import BiPart

class UserPostGraph(PropGraph,BiPart):

	def doCompoCluster(self,compo_prop='compo',clust_prop='clust', algo='fastgreedy'):
		vertices={v['name']:v for v in self.vs}
		self.simplify()
		compos=self.components().subgraphs()
		for i,compo in enumerate(compos):
			for v in compo.vs:
				v[compo_prop]=i
			clusts=self.__doClustering__(compo,algo)
			for j,vs in enumerate(clusts):
				for v in vs:
					vertices[v['name']][compo_prop]=i
					vertices[v['name']][clust_prop]=j

	def __doClustering__(self, g, algo):
		g.to_undirected()
		clusts=[]
		
		subgraphs=None
		if algo=='fastgreedy':
			subgraphs=g.community_fastgreedy().as_clustering().subgraphs()
		elif algo=='eigenvector':
			subgraphs=g.community_leading_eigenvector().subgraphs()
		else:
			raise Exception('Algo is clustering algo illegal')
		
		for clust in subgraphs:
			clusts.append([v for v in clust.vs])

		return clusts
		
	'''Implementing BiPart abstract functions'''
	def left(self):		
		return [v for v in self.vs if v['name'][0]=='u']

	def right(self):
		return [v for v in self.vs if v['name'][0]=='p']
		return

	def isLeft(self,v):
		return v['name'][0]=='u'

	def isRight(self,v):
		return  v['name'][0]=='p'