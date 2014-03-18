from igraph import *

f_inputgraph='/tmp/soclust/weekgraph/%d.graphml'
f_outputgraph='/tmp/soclust/weekgraph/cowatch/%d.graphml'

def main():
	g=Graph.Read_GraphML(f_inputgraph%200924)
	g0=g.subgraph([v for v in g.vs if v['compo']==0])
	g0_cowatch=buildCoWatcherWeight(g0)
	g0_cowatch.write_graphml(f_outputgraph%200924)

def buildCoWatcherWeight(g):

	vdocs=[v for v in g.vs if v['name'][0]=='p']
	g_cowatch=Graph()
	g_cowatch=g.subgraph(vdocs)
	for i in range(len(vdocs)):
		nb1=g.neighbors(vdocs[i])
		for j in range(i+1,len(vdocs)):
			nb2=g.neighbors(vdocs[j])
			cowatcher=set(nb1).intersection(set(nb2))
			if len(cowatcher) > 0:
				g_cowatch.add_edge(i,j,cowatch_len=len(cowatcher))

	return g_cowatch	

if __name__ =='__main__':
	main()
