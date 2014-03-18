'''
Do KMeans clustering over given documents using lemur (in parallel)
Input: 
	-i: input csv file(post_id	message)
	-o:	output csv file(post_id	clust_id)
	-clust: number of clusters documents will be partitioned into
'''

import os
import argparse
import re
import csv

f_index_param='/proj/DSL/sincere/big-server/_gited/soclust/lemur_clust/lemur-index-param.xml'

f_input=''
f_output=''
clustCount=0


def main():

	parser=argparse.ArgumentParser()
	parser.add_argument("input_file",help="Input csv file (post_id,post_message")
	parser.add_argument("output_file",help="Output csv file (post_id,cluster_id")
	parser.add_argument("clust_no",help="Number of clusters wanted", type=int)
	args=parser.parse_args()
	f_input=args.input_file
	f_output=args.output_file
	clustCount=args.clust_no
	
	posts=[]
	with open(f_input,'r') as f:
		reader=csv.DictReader(f,['post_id','message'],delimiter='\t')
		for row in reader:
			if row['post_id'][0]=='#':
				continue
			posts.append(row)
	
	
	f_trec=f_output+'.trec'
	getTREC(posts,f_trec)
	
	os.system("sudo rm -f kindex*")
	os.system("sudo /mnt/large/cnnfox/lemur/app/obj/BuildIndex  %s %s"%(f_index_param,f_trec))
	
	f_output_lemur=f_output+'.lemur'
	doKMeansCluster(f_output_lemur,clustCount)
	lemur2csv(f_output_lemur,f_output)
	
	os.system('sudo rm %s %s'%(f_output_lemur,f_trec))

def doKMeansCluster(f_output_lemur,clustCount):
	f_param=f_output+'.param'
	with open(f_param,'w') as f:
		f.write("<parameters><index>kindex.key</index><clusterType>centroid</clusterType><numParts >%d</numParts ></parameters>" %clustCount)	
		f.close()
	
	os.system("sudo /mnt/large/cnnfox/lemur/app/obj/OfflineCluster %s > %s"%(f_param,f_output_lemur))
	os.system("sudo rm %s"%f_param)

'''
Create TREC file containing given posts
Input:
	posts: list of dicts {post_id:id, message:content}	
'''
def getTREC(posts,f_trec):
	
	with open(f_trec,'w') as f:
		for post in posts:
			f.write('<DOC>\n')
			f.write('<DOCNO>%s</DOCNO>\n'%post['post_id'])
			f.write('%s\n'%post['message'])
			f.write('</DOC>\n')

def lemur2csv(f_output_lemur,f_output):
	
	reg=re.compile('^(\d+)\(\d+\):')
	pid_clustid={}
	with open(f_output_lemur,'r') as f:
		for l in f:
			m=reg.match(l)
			if not m: continue
			groupid=m.group(1)
			l=l[m.end():]
			pid_clustid.update({e:groupid for e in l.split()})
	with open(f_output,'w') as f:
		writer=csv.writer(f,delimiter='\t')
		writer.writerow(['#post_id','lemur_cluster'])
		for pid,clust in pid_clustid.items():
			writer.writerow([pid,clust])
			
	
if __name__=='__main__':
	main()




