import MySQLdb

db=MySQLdb.connect(host='localhost',user='root',passwd='toor',db='so')
cur=db.cursor()
cur.execute('SELECT Tags,Id FROM posts__ WHERE Tags IS NOT NULL')

tags={}
for row in cur.fetchall():
	ts= ('>'+row[0]+'<').split('><')
	for t in [t for t in ts if len(t)]:
		if t not in tags:
			tags[t]=[row[1]]
		else:
			tags[t].append(row[1])

####
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.figure()

plt.hist([len(pts) for t,pts in tags5.items()], bins=1000)

plt.savefig
plt.xlabel('posts per tag')
plt.ylabel('number of tags')
plt.yscale('log')
plt.xscale('log')
plt.title('Post count per tag')
plt.savefig('/tmp/so/tags5_distrib.png')

####

edges=[]

for t,pts in tags.items():
	for p in pts:
		edges.append(('t'+str(t),'p'+str(p)))


from igraph import Graph
g=Graph.TupleList(edges)



