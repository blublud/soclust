#!/bin/python
import sys;sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/igraph_extension')
from userpostgraph import UserPostGraph
import MySQLdb

db=MySQLdb.connect(host='localhost',user='root',passwd='toor',db='nyt')

#sql_getvotes='SELECT CONCAT("u",fb_id),CONCAT("p",post_id) FROM comment WHERE post_id IN (SELECT id FROM post WHERE YEARWEEK(created_time)=201253);'

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
	g.clust_nmf(clust_on_side='r',n_features=min(users,10),n_clust=4)
	#g.cluster_tiestrength_kmeans(vertices=g.right(),nclusters=2,cluster_prop='tsk')
	g=g.induced_subgraph(g.right())
	#g.write_graphml('/tmp/nyt/graphml.graphml')
	#write_csv('/scratch/DSL/sincere-big-server/tmp/nmf_201253.csv', g,['nmf','tsk','msg'])
	write_csv('/scratch/DSL/sincere-big-server/tmp/nmf_201253_4clust.csv', g,['nmf','msg','time'])

def weight_likecount():
	sql_likecount='SELECT DISTINCT CONCAT("u",c.fb_id),CONCAT("p",c.post_id),likecount FROM comment AS c JOIN (SELECT post_id,comment_id, COUNT(*) as likecount FROM likedby WHERE post_id IN (SELECT id FROM post WHERE  YEARWEEK(created_time)=201253) GROUP BY post_id,comment_id HAVING likecount > 2) AS l ON c.post_id=l.post_id AND c.id=l.comment_id;'
	cur=db.cursor()
	cur.execute(sql_likecount)
	edges=[(row[0],row[1],row[2]) for row in cur.fetchall()] #row[0]=user;row[1]=post;row[2]=weight
	g=UserPostGraph.TupleList(edges,directed=False)
	g.loadPropsFromFile(fProp='/tmp/nyt/post_msg_201253.csv',propName='msg')
	non_active_users=[]
	for user in g.left():
		if user.degree()<4 or user.degree()>10:
			non_active_users.append(user.index)
	g.delete_vertices(non_active_users)
	users=len(g.left())
	print '#users:',users
	g.clust_nmf(clust_on_side='r',n_features=min(users,10),n_clust=2)
	g.cluster_tiestrength_kmeans(vertices=g.right(),nclusters=2,cluster_prop='tsk')
	g=g.induced_subgraph(g.right())
	#g.write_graphml('/tmp/nyt/graphml.graphml')
	write_csv('/scratch/DSL/sincere-big-server/tmp/nmf_201253.csv', g,['nmf','tsk','msg'])

def write_csv(fname,g,fields=[]):
	from csv import writer
	with open(fname,'w') as f:
		w=writer(f,delimiter='\t')
		for v in g.vs:
			row=[v[attrib]for attrib in fields]
			w.writerow(row)

if __name__=='__main__':
	main()
