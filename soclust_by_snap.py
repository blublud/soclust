import csv
import os
'''
Convert from fbid 2 seq
Input:edges list (using fbid) in csv format
Output: 2 dicts fb2seq {fbid->seq}, seq2fb {seq->fbid}
'''
def fbid2seq(csvfile):
	f2s={}
	s2f={}
	with open(csvfile,'rb') as f:
		r=csv.reader(f,delimiter="\t")
		for row in r:
			fbid=row[0]
			if fbid not in f2s:
				seq=str(len(f2s))
				f2s[fbid]=seq
				s2f[seq]=fbid
			fbid=row[1]
			if fbid not in f2s:
				seq=str(len(f2s))
				f2s[fbid]=seq
				s2f[seq]=fbid

	return f2s,s2f

def main():
	csvfile='/mnt/large/cnnfox/CNN-comment.csv'
	labelfile='/mnt/large/cnnfox/CNN-comment-label.csv'
	edgefile='/mnt/large/cnnfox/CNN-comment-edge.csv'
	snap_cmd='sudo /mnt/large/snap/Snap-2.1/examples/agmfit/agmfitmain -i:%s -l:%s -o:cnn'%(edgefile,labelfile)
	#read csv edges file => output edges by seq file, output nodes label	
	f2s,s2q=fbid2seq(csvfile)
	
	flabel=open(labelfile,'w')
	for s,f in s2q.items():
		flabel.write(s+"\t"+f + "\n")
	flabel.close()

	fedge=open(edgefile,'w')
	with open(csvfile,'rb') as f:
		r=csv.reader(f,delimiter="\t")
		for row in r:
			f1=f2s[row[0]]
			f2=f2s[row[1]]
			fedge.write(f1+"\t"+f2+"\n")

	fedge.close()
	
	os.system(snap_cmd)

if __name__ == "__main__":
	main()
