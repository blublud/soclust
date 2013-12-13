#!/bin/python3
import os
from concurrent import futures

def doKMeansCluster(k):
	print ("Start %d-clustering" %k)
	paramFile=open("/tmp/cnnfox/lemur-cluster-param-%d.xml"%k,'w')
	paramFile.write("<parameters><index>kindex.key</index><clusterType>centroid</clusterType><numParts >%d</numParts ></parameters>" %k)	
	paramFile.close()
	res=os.system("sudo /mnt/large/cnnfox/lemur/app/obj/OfflineCluster /tmp/cnnfox/lemur-cluster-param-%d.xml > /tmp/cnnfox/lemur-cluster-%d.clust"%(k,k))
	os.system("sudo cp /tmp/cnnfox/lemur-cluster-%d.clust /scratch/DSL/sincere-big-server/cnnfox/"%k)
	if res:
		print ("%d-clustering cannot be done"%k)
	else:
		os.system("sudo cp /tmp/cnnfox/lemur-cluster-%d.clust /scratch/DSL/sincere-big-server/cnnfox/"%k)
		os.system("sudo rm /tmp/cnnfox/lemur-cluster-param-%d.xml"%k)

with futures.ProcessPoolExecutor(max_workers=32) as executor:
	for i in executor.map(doKMeansCluster, range(1000,2000, 10)):
		pass

