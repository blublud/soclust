from igraph import *
import cPickle
import os

os.system('mkdir -p /mnt/large/cnnfox/cnn-soclust/')
g=Graph.Read_Ncol('/mnt/large/cnnfox/CNN-comment.csv')
g.to_undirected()
dendogram=g.community_fastgreedy()
cPickle.dump(dendogram,open('/mnt/large/cnnfox/cnn-soclust/cnn-dendogram.dat', 'w'))
os.system("/proj/DSL/sincere/big-server/scriptlib/copy-retry.sh /mnt/large/cnnfox/cnn-soclust/cnn-dendogram.dat /scratch/DSL/sincere-big-server/cnnfox/soclust")

for k in range(2,1000, 10):
	try:
		clust=dendogram.as_clustering(k)
		f=open('/mnt/large/cnnfox/cnn-soclust/soclust-%03d'%k,'w')
		for i,subg in enumerate(clust.subgraphs()):
			for v in subg.vs:
				f.write(v['name']+"\t"+str(i)+"\n")
			f.close()
	except Exception as e:
		print("Error at k=%d. %s"%(k,e.strerr))

os.system("/proj/DSL/sincere/big-server/scriptlib/backup.sh /mnt/large/cnnfox/cnn-soclust/ /scratch/DSL/sincere-big-server/cnnfox/soclust soclust")

