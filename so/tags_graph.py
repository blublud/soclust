import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.figure()

import sys; sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/igraph_extension');
from bipart import BiPart

import MySQLdb

db=MySQLdb.connect(host='localhost',user='root',passwd='toor',db='so')
cur=db.cursor()
#cur.execute('SELECT Tags,Id FROM posts1212 WHERE Tags IS NOT NULL')
cur.execute('SELECT Tags,Id FROM posts WHERE Tags IS NOT NULL AND Year(CreationDate)=2012')

tags={}
for row in cur.fetchall():
	ts= ('>'+row[0]+'<').split('><')
	for t in [t for t in ts if len(t)]:
		if t not in tags:
			tags[t]=[row[1]]
		else:
			tags[t].append(row[1])

tags={t:pts for t,pts in tags.items() if len(pts) > 10}
edges=[]

for t,pts in tags.items():
	for p in pts:
		edges.append(('t'+str(t),'p'+str(p)))


g=BiPart.TupleList(edges,directed=True)

trim_t=0.1
vtags=[v for v in g.vs if v['name'][0]=='t']
gts=g.graph_commonNeighbors(vtags, trim_threshold=trim_t)

gts.write_graphml('/tmp/so/taggraph.graphml'%trim_t)


'''
weights=[e['weight'] for e in gts.es]
#plot weight distribution
plt.hist(weights, bins=1000)
plt.savefig
plt.xlabel('weight')
plt.ylabel('frequency')
#plt.yscale('log')
#plt.xscale('log')
plt.title('SO Tags:weight distribution of common_neighbor graph')
plt.savefig('/tmp/so/tags_graph_weight_distrib_%f.png'%trim_t)
#end plot weight distribution
'''

