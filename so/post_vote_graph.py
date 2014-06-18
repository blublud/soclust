#!/bin/python

############
#build graph
############
import MySQLdb

db=MySQLdb.connect(host='localhost',user='root',passwd='toor',db='so')
cur=db.cursor()
cur.execute('SELECT CONCAT("u",UserId),CONCAT("p",PostId) FROM votes1212')

edges=[(row[0],row[1]) for row in cur.fetchall()] #row[0]=user;row[1]=post

import sys; sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/igraph_extension');
from bipart import BiPart

g=BiPart.TupleList(edges,directed=False)


