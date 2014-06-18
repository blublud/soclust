####
import sys; sys.path.append('/proj/DSL/sincere/big-server/_gited/soclust/select_by_event/igraph_inheritance');
from bipart import BiPart

trim_t=0.1
sub_tag_t=0.5
g=BiPart.Read_GraphML('/scratch/DSL/sincere-big-server/tmp/sotags2012_%f.graphml'%trim_t)
n=g.vcount()
x=g.katz_centrality()
idx_ranked=[ic[0] for ic in sorted(enumerate(x), key=lambda ic:ic[1]) ]

intree_tags={} #k:[ancestor0,ancestor1]

for tag in idx_ranked:
	my_level=-1
	my_neighbors=[nb for nb in g.neighbors(tag,mode=1) if nb in intree_tags]
	if len(my_neighbors): 
		print len(my_neighbors)
	my_sup=-1 #root
	cont=True
	while(cont):
		cont=False
		my_level+=1
		neighbor_ancestors=[intree_tags[nb][my_level] for nb in my_neighbors if len(intree_tags[nb]) > my_level]
		ancestor_coverages={a:0.0 for a in neighbor_ancestors}
		max_coverage=sub_tag_t #=0.8
		for i,a in enumerate(neighbor_ancestors):
			ancestor_coverages[a]+=g.es[g.get_eid(tag,my_neighbors[i])]['weight']
			if ancestor_coverages[a] > max_coverage:
				max_coverage=ancestor_coverages[a]
				my_sup=a
				cont=True
	if my_sup==-1:
		intree_tags[tag]=[tag]
	else:
		intree_tags[tag]=intree_tags[my_sup]+[my_sup,tag]

gg=g.copy()
gg.delete_edges(gg.es)
es=[(t,ancestors[-2]) for t,ancestors in intree_tags.items() if len(ancestors)>1]
for (s,t) in es:
	gg.add_edge(s,t)

gg.write_graphml('/scratch/DSL/sincere-big-server/tmp/tag_hierachy2012.graphml')


#ranked_tags=[g.vs[i]['name'][1:] for i in idx_ranked]
