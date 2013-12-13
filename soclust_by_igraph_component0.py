from igraph import *
import cPickle
import os

'''
os.system('mkdir -p /mnt/large/cnnfox/cnn-soclust/')
g=Graph.Read_Ncol('/mnt/large/cnnfox/CNN-comment.csv')
g.to_undirected()
g0=g.components().subgraphs()[0]
dendogram=g0.community_fastgreedy()
cPickle.dump(dendogram,open('/mnt/large/cnnfox/cnn-soclust/cnn-dendogram-c0.dat', 'w'))
os.system("/proj/DSL/sincere/big-server/scriptlib/copy-retry.sh /mnt/large/cnnfox/cnn-soclust/cnn-dendogram-c0.dat /scratch/DSL/sincere-big-server/cnnfox/soclust")
'''
dendogram = cPickle.load(open('/mnt/large/cnnfox/cnn-soclust/cnn-dendogram-c0.dat', 'r'))

for k in range(2,1000, 10):
	try:
		clust=dendogram.as_clustering(k)
		f=open('/mnt/large/cnnfox/cnn-soclust/soclust-%04d'%k,'w')
		for i,subg in enumerate(clust.subgraphs()):
			for v in subg.vs:
				f.write(v['name']+"\t"+str(i)+"\n")
		f.close()
	except Exception as e:
		print("Error at k=%d. %s"%(k,str(e)))

os.system(" /proj/DSL/sincere/big-server/scriptlib/backup.sh /mnt/large/cnnfox/cnn-soclust/ /scratch/DSL/sincere-big-server/cnnfox/soclust soclust")

