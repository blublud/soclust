from igraph import Graph
import numpy as np

class BiPart(Graph):

'''
	This function produces the matrix of common neighbor between set of vertices 
'''
	def commonNeighbors(vertices):
		size=len(vertices)
		cn=np.zeros((size,size))
		
		for i in range(size):
			for j in range(i+1,size):
				cn[i,j]=len(set(vertices[i].neighbors()) & set(vertices[j].neighbors()))
				
		return cn