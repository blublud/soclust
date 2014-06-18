import matplotlib
matplotlib.use('Agg')

import sys;sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/igraph_extension')
from userpostgraph import UserPostGraph

from sys import path;path.append('/proj/DSL/sincere/big-server/_gited/soclust/_test/sklearn_extension/')
from nmf import NMF_GetAll

from sys import path;path.append('/proj/DSL/sincere/big-server/_gited/soclust/_test/')
from dendro_path import dendro_path

import MySQLdb

import scipy.cluster.hierarchy as sch
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import pairwise_distances

db=MySQLdb.connect(host='localhost',user='root',passwd='toor',db='nyt')

###
db=MySQLdb.connect(host='localhost',user='root',passwd='toor',db='nyt')

sql_userpost_cond_postcount=\
'''SELECT CONCAT("u",c.fb_id),CONCAT("p",c.post_id) 
FROM
	(SELECT DISTINCT c.fb_id, c.post_id
	FROM comment c 
	WHERE YEARWEEK(created_time)=201253 
	) AS c 
	JOIN
	(SELECT fb_id
	FROM comment 
	WHERE YEARWEEK(created_time)=201253
	GROUP BY fb_id
	HAVING COUNT( DISTINCT post_id) > 5
	) AS u
	ON c.fb_id=u.fb_id'''

sql_getvotes='SELECT DISTINCT CONCAT("u",c.fb_id),CONCAT("p",c.post_id) FROM comment AS c JOIN (SELECT post_id,comment_id, COUNT(*) as likecount FROM likedby WHERE post_id IN (SELECT id FROM post WHERE  YEARWEEK(created_time)=201253) GROUP BY post_id,comment_id HAVING likecount > 1) AS l ON c.post_id=l.post_id AND c.id=l.comment_id;'
cur=db.cursor()
cur.execute(sql_userpost_cond_postcount)
edges=[(row[0],row[1]) for row in cur.fetchall()] #row[0]=user;row[1]=post
g=UserPostGraph.TupleList(edges,directed=False)
g.loadPropsFromFile(fProp='/tmp/nyt/post_msg_201253.csv',propName='msg')
g.loadPropsFromFile(fProp='/tmp/nyt/post_time_201253.csv',propName='time')
non_active_users=[]
for user in g.left():
	#if user.degree()<4 or user.degree()>10:
	if user.degree()<3:#4:is good for 2012_51 week
		non_active_users.append(user.index)

g.delete_vertices(non_active_users)
users=len(g.left())
print '#users:',users
g.fix_bipart_vindex()
a=g.get_adjacency('lr')
nmf=NMF_GetAll(n_components=min(users,10))
U,D=nmf.fit_transform(a)
D=D.transpose()
D=normalize(D,axis=1)
distances=pairwise_distances(D,metric='euclidean')
Y = sch.linkage(distances, method='centroid')

g.clust_nmf(clust_on_side='r',clust_prop='nmf',n_features=min(users,10),n_clust=4)
#plot

import pylab
fig=pylab.figure(figsize=(8,8))

ax1 = fig.add_axes([0.09,0.1,0.2,0.6])
Z1=sch.dendrogram(Y,orientation='right')
ax1.set_xticks([])
doc_vertices=g.right()
ax1.set_yticklabels([doc_vertices[v]['nmf']for v in Z1['leaves']],size=5)

axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])
idxdoc=Z1['leaves']
a=a[:,idxdoc]
axmatrix.minorticks_on()
axmatrix.grid(b=True,which='both')
im = axmatrix.matshow(a.transpose().todense(), aspect='equal', origin='lower', cmap=pylab.cm.YlGnBu)
#axmatrix.set_xticks([])
#axmatrix.set_yticks([])


fig.savefig('/scratch/DSL/sincere-big-server/tmp/dendro_mat_201253.png')
g.write_csv('/scratch/DSL/sincere-big-server/tmp/nmf_201253.csv',['nmf','msg','time'],g.right())

'''
###
def main():
	#weight_likecount()
	nmf()

def nmf():
	db=MySQLdb.connect(host='localhost',user='root',passwd='toor',db='nyt')
	sql_getvotes='SELECT DISTINCT CONCAT("u",c.fb_id),CONCAT("p",c.post_id) FROM comment AS c JOIN (SELECT post_id,comment_id, COUNT(*) as likecount FROM likedby WHERE post_id IN (SELECT id FROM post WHERE  YEARWEEK(created_time)=201253) GROUP BY post_id,comment_id HAVING likecount > 1) AS l ON c.post_id=l.post_id AND c.id=l.comment_id;'
	cur=db.cursor()
	cur.execute(sql_getvotes)
	edges=[(row[0],row[1]) for row in cur.fetchall()] #row[0]=user;row[1]=post
	g=UserPostGraph.TupleList(edges,directed=False)
	g.loadPropsFromFile(fProp='/tmp/nyt/post_msg_201253.csv',propName='msg')
	g.loadPropsFromFile(fProp='/tmp/nyt/post_time_201253.csv',propName='time')
	non_active_users=[]
	for user in g.left():
		#if user.degree()<4 or user.degree()>10:
		if user.degree()<3:#4:is good for 2012_51 week
			non_active_users.append(user.index)
	g.delete_vertices(non_active_users)
	users=len(g.left())
	print '#users:',users
	a=g.get_adjacency('lr')
	nmf=NMF_GetAll(n_components=min(users,10))
	U,D=nmf.fit_transform(a)
	D=D.transpose()
	D=normalize(D,axis=1)
	distances=pairwise_distances(R,metric='euclidean')
	Y = sch.linkage(distances, method='centroid')
	
	
	#plot
	import matplotlib
	matplotlib.use('Agg')
	import pylab
	fig=pylab.figure(figsize=(8,8))
	ax1 = fig.add_axes([0.09,0.1,0.2,0.6])
	Z1=sch.dendrogram(Y,orientation='right')
	ax1.set_xticks([])
	ax1.set_yticks([])
	
	axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])
	idxdoc=Z1['leaves']
	a=a[:,idxdoc]
	im = axmatrix.matshow(D, aspect='auto', origin='lower', cmap=pylab.cm.YlGnBu)
	axmatrix.set_xticks([])
	axmatrix.set_yticks([])
	
	fig.savefig('/scratch/DSL/sincere-big-server/tmp/dendro_mat_201253.png')
	
'''
