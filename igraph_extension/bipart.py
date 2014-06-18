from igraph import Graph
import numpy as np
import abc
from sklearn.cluster import Ward
from scipy.spatial.distance import cdist
from scipy.sparse import lil_matrix

import sys; sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/igraph_extension');
from centrality import Centrality
from clustering import Clustering

import propgraph

from sys import path;path.append('/proj/DSL/sincere/big-server/_gited/soclust/_test/sklearn_extension/')
from nmf import NMF_GetAll

from sklearn.metrics.pairwise import pairwise_distances
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize

class BiPart(Centrality):
	
	__nameprop='name'
	__weightprop='weight'
	__metaclass__ = abc.ABCMeta
	'''
		This function produces the matrix of common neighbor between set of vertices 
	'''

	def loadProperties(self, vertex_propVals,propName,id_prop='name'):
		propgraph.loadProperties(self,vertex_propVals,propName,id_prop)
	
	def loadPropsFromFile(self, fProp, propName,id_prop='name',delim='\t'):
		propgraph.loadPropsFromFile(self,fProp,propName,id_prop,delim)
	
	'''
	Export vertices' properties to .csv file
	Input:
	fname:
	fields: list of properties' names
	vertices: list of vertices needed exporting. If None then all vertices are exported
	'''
	def write_csv(self, fname,fields=[], vertices=None):
		if vertices is None:
			vertices=self.vs
		
		from csv import writer
		with open(fname,'w') as f:
			w=writer(f,delimiter='\t')
			for v in vertices:
				row=[v[attrib]for attrib in fields]
				w.writerow(row)

	def commonNeighbors(self,vertices):
		size=len(vertices)
		cn=np.zeros((size,size))
		
		viewers=self.neighborhood([ v.index for v in vertices])
		for i in range(size):
			for j in range(i+1,size):
				conb=len(set(viewers[i]) & set(viewers[j]))
				if not conb: continue
				cn[i,j]=float(conb)/len(set(viewers[i]))
				cn[i,j]=float(conb)/len(set(viewers[j]))
				#cn[i,j]=len(set(viewers[i]) & set(viewers[j]))
				
		return cn

	def commonNeighborsTrimmed(self, vertices, trim_threshold=0.1):
		size=len(vertices)
		cn=np.zeros((size,size))
		
		viewers=self.neighborhood([ v.index for v in vertices])
		for i in range(size):
			for j in range(i+1,size):
				conb=len(set(viewers[i]) & set(viewers[j]))
				if not conb: continue
				ij=float(conb)/len(set(viewers[i]))
				ji=float(conb)/len(set(viewers[j]))
				if ij > ji and ij >= trim_threshold:
					cn[i,j]=ij
				elif ji > ij and ji >= trim_threshold:
					cn[j,i]=ji
				
		return cn
		
	def graph_commonNeighbors(self, vertices,trim_threshold=0.1):
		
		data=self.commonNeighborsTrimmed(vertices,trim_threshold)
		nwEdges=[]
		for i in range(len(vertices)):
			for j in range(len(vertices)):
				if data[i][j] >= trim_threshold:
					nwEdges.append((vertices[i][self.__nameprop],vertices[j][self.__nameprop],data[i][j]))

		g=BiPart.TupleList(nwEdges,directed=True,weights=True)
		return g

	@abc.abstractmethod
	def left(self):
		'''Return the vertices of the left part'''
		return
	@abc.abstractmethod
	def right(self):
		'''Return the vertices of the right part'''
		return
	@abc.abstractmethod
	def isLeft(self,v):
		return
	@abc.abstractmethod
	def isRight(self,v):
		return
		
	'''
		LEFT: users
		RIGHT: posts
	'''
	__l_n2i=None;__l_i2n=None
	__r_n2i=None;__r_i2n=None
	def fix_bipart_vindex(self):
		self.__l_n2i={};self.__l_i2n=[]
		self.__r_n2i={};self.__r_i2n=[]
		lnodes=self.left()
		rnodes=self.right()
		for v in lnodes:
			self.__l_i2n.append(v[self.__nameprop])
			self.__l_n2i[v[self.__nameprop]]=len(self.__l_i2n)-1
		for v in rnodes:
			self.__r_i2n.append(v[self.__nameprop])
			self.__r_n2i[v[self.__nameprop]]=len(self.__r_i2n)-1
	
	def doCoClustering(self,leftClustCount,rightClustCount,clustPropName='coclust'):
		
		vsleft=self.left()
		simleft=np.matrix(self.similarity_dice(vsleft))
		clustleft=Ward(n_clusters=leftClustCount).fit(simleft).labels_
		
		vsright=self.right()
		full2bipart=[(None,-1)]*self.vcount()#tuple of (isOnRightSide,index in left/right list)
		for i,v in enumerate(vsleft):
			full2bipart[v.index]=(False,i)
		for i,v in enumerate(vsright):
			full2bipart[v.index]=(True,i)
			
		sizeright=len(vsright)
		m_rclust=np.zeros(shape=(sizeright,leftClustCount))
		for e in self.es:
			(srcOnRight,src)=full2bipart[e.source]
			(_,dst)=full2bipart[e.target]
			if srcOnRight:
				vright=src
				clust=clustleft[dst]
			else:
				vright=dst
				clust=clustleft[src]
				
			m_rclust[vright,clust]+=1
		
		clustSizes=[0]*leftClustCount
		for c in clustleft: 
			clustSizes[c]+=1
			
		for (row,col) in [(row,col) for (row,col),val in np.ndenumerate(m_rclust) if val]:
			#m_rclust[row,col]=float(val)/clustSizes[col]
			m_rclust[row,col]=float(val)/vsright[row].degree()
		
		simRight=cdist(m_rclust,m_rclust,'cosine')
		clustright=Ward(n_clusters=rightClustCount).fit(simRight).labels_
		
		for i,c in enumerate(clustright):
			vsright[i][clustPropName]=c
			
	def get_adjacency(self, dimension='lr'):
		'''
		Get the adjacency matrix of the bipartie graph
		Parameters:
		----------
		deimension: can be either 'lr' or 'rl', specifies the dimension of the returned matrix
		(lxr or rxl)
		Returns:
		the adjacency matrix with the dimension as specified
		'''
		if dimension not in ('lr','rl'):
			raise ValueError('Invalid dimension specification')
		if self.__l_n2i==None:
			raise ValueError('Bipartie indices have not been generated')
		if len(self.__l_n2i)!=len(self.__l_i2n) or len(self.__r_n2i) != len(self.__r_i2n):
			raise ValueError('Bipartie indices are not consistent')
		
		left_count=len(self.__l_i2n)
		right_count=len(self.__r_i2n)
		a=lil_matrix((left_count,right_count))
		for e in self.es:
			if self.__weightprop in e.attribute_names():
				weight=e[self.__weightprop]
			else:
				weight=1
			if self.isLeft(self.vs[e.source]):
				row=self.__l_n2i[self.vs[e.source][self.__nameprop]]
				col=self.__r_n2i[self.vs[e.target][self.__nameprop]]
				a[row,col]=weight
			else:
				row=self.__l_n2i[self.vs[e.target][self.__nameprop]]
				col=self.__r_n2i[self.vs[e.source][self.__nameprop]]
				a[row,col]=weight
		
		if dimension =='rl':
			a=a.transpose()
		return a

	def doCompoCluster(self,compo_prop='compo',clust_prop='clust', algo='fastgreedy'):
		vertices={v['name']:v for v in self.vs}
		self.simplify()
		compos=self.components().subgraphs()
		for i,compo in enumerate(compos):
			for v in compo.vs:
				v[compo_prop]=i
			clusts=self.__doCompoCluster__(compo,algo)
			for j,vs in enumerate(clusts):
				for v in vs:
					vertices[v['name']][compo_prop]=i
					vertices[v['name']][clust_prop]=j

	def __doCompoCluster__(self, g, algo):
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

	def cluster_tiestrength_kmeans(self,vertices=None, nclusters=2, cluster_prop='tsk'):
		if vertices is None:
			vertices=self.gs
		ts=self.similarity_dice(vertices) #list of list of similarity(float)
		ward=Ward(nclusters).fit(ts)
		for i,v in enumerate(vertices):
			v[cluster_prop]=ward.labels_[i]


	def clustereval_weightedsumentropy(self, vertices=None, ground_truth_prop='ground_prop',eval_prop='eval_prop'):
		if vertices==None:
			vertices=self.vs
		eval_labels={}
		for v in vertices:
			ground_label=v[ground_truth_prop]
			if  ground_label not in eval_labels:
				eval_labels[ground_label]=[v[eval_prop]]
			else:
				eval_labels[ground_label].append(v[eval_prop])

		wse=0
		vcount=len(vertices)
		for ll in eval_labels.values():
			wse+=float(len(ll))/vcount *__entropy__(ll)
		
		return wse

	def clustereval_adjustedRand(self,vertices=None, ground_truth_prop='ground_prop',eval_prop='eval_prop'):
		if vertices==None:
			vertices=self.vs
		labels_ground=[v[ground_truth_prop] for v in vertices]
		labels_eval=[v[eval_prop] for v in vertices]
		return metrics.adjusted_rand_score(labels_ground,labels_eval)

	def clustereval_mutualinfo(self,vertices=None, ground_truth_prop='ground_prop',eval_prop='eval_prop'):
		if vertices==None:
			vertices=self.vs
		labels_ground=[v[ground_truth_prop] for v in vertices]
		labels_eval=[v[eval_prop] for v in vertices]
		return metrics.adjusted_mutual_info_score(labels_ground,labels_eval)

	def clust_nmf(self,clust_on_side='l',clust_prop='nmf',n_features=20,n_clust=10):
		'''
		Do clustering on the bipartie graph using nmf factorization.
		Parameters:
		clust_on_side: can be either 'l' or 'r'. Spcifying the side of bipartie graph to be clustered.
		clust_prop: the clustering result is saved as a property in the nodes. clust_prop specifies the name of the propery to be saved.
		n_features: l-by-r adjacency matrix is factored as l-by-n_features * n_features-by-m
		n_clust: the desired number of clusters.
		'''
		if clust_on_side not in ('l','r'):
			raise ValueError('clust_on_side must be either "l" or "r"')
		if not (type(clust_prop) is str and len(clust_prop) > 0):
			raise ValueError('clust_prop is not valid')
		if (n_features <=0):
			raise ValueError('n_features must be > 0')
		
		self.fix_bipart_vindex()
		a=self.get_adjacency('lr')
		nmf=NMF_GetAll(n_components=n_features)
		L,R=nmf.fit_transform(a)
		'''
		#This snipet uses argmax
		if clust_on_side=='l':
			labels=np.argmax(L,1)
			for i,v in enumerate(self.left()):
				v[clust_prop]=labels[i]
		else:
			labels=np.argmax(R,0)
			for i,v in enumerate(self.right()):
				v[clust_prop]=labels[i]
		'''
		'''
		#This snippet uses kmeans
		if clust_on_side=='l':
			normalize(L,axis=1)
			distances=pairwise_distances(L,metric='euclidean')
		else:
			R=R.transpose()
			R=normalize(R,axis=1)
			distances=pairwise_distances(R,metric='euclidean')
		kclust=KMeans(n_clusters=n_clust)
		kclust.fit(distances)
		if clust_on_side=='l':
			vertices_to_find=self.left()
		else:
			vertices_to_find=self.right()
		for i,label in enumerate(kclust.labels_):
			vertices_to_find[i][clust_prop]=label
		'''
		
		#this snipet uses hac
		if clust_on_side=='l':
			normalize(L,axis=1)
			distances=pairwise_distances(L,metric='euclidean')
		else:
			R=R.transpose()
			R=normalize(R,axis=1)
			distances=pairwise_distances(R,metric='euclidean')
		import sys; sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/_test')
		from dendro_path import dendro_path
		import scipy.cluster.hierarchy as sch
		Y = sch.linkage(distances, method='centroid')
		ahc_traces=dendro_path(sch.to_tree(Y))
		if clust_on_side=='l':
			vertices_to_find=self.left()
		else:
			vertices_to_find=self.right()
		for i,trace in ahc_traces.items():
			vertices_to_find[i][clust_prop]=trace
		

	def katz_centrality(self, alpha=1.0):
		n=self.vcount()
		import numpy as np
		a=np.zeros((n,n),dtype=float)

		for e in self.es:
			a[e.source,e.target]=e['weight']
		
		x=np.linalg.solve(np.eye(n) -alpha*a, np.ones(n))
		return x

	'''
		Print the common neighbor matrix together with some vertex's properties 
	'''
'''	
	def commonNeighborGraph(self,vertices):
		g=self.induced_subgraph(vertices)
		cn=commonNeighbors(self,vertices)
		for i in range(g.vcount()):
			for j in range(g.vcount()):
				if cn[i,j]:
					g.
					
'''
