import sys;sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/igraph_extension')
import numpy as np
from sklearn.cluster import Ward
from sklearn import metrics
import math


def __entropy__(labels):
	size=len(labels)
	distrib={}
	for l in labels:
		if l not in distrib:
			distrib[l]=1
		else:
			distrib[l]+=1

	entropy=0
	for v in distrib.values():
		prop=float(v)/size
		entropy+=prop*math.log(prop)

	return -1*entropy


class Clustering:

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

	def cluster_tiestrength_kmeans(self,vertices=None, nclusters=2, cluster_prop='cprop'):
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

