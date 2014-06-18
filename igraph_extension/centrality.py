from igraph import *
import csv
class Centrality(Graph):

	def katz_centrality(self, alpha=1.0):
		n=self.vcount()
		import numpy as np
		a=np.zeros((n,n),dtype=float)

		for e in self.es:
			a[e.source,e.target]=e['weight']
		
		x=np.linalg.solve(np.eye(n) -alpha*a, np.ones(n))
		return x

