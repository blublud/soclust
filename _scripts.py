
#convert lemur -> csv
lemur2csv('/tmp/cnnfox/lemur-cluster-170.clust','/tmp/lemur-170.csv')
#batch convert lemur -> csv
sys.path.append('/proj/DSL/sincere/big-server/cnnfox/')
import soctoc as st 
for f in os.listdir('/scratch/DSL/sincere-big-server/cnnfox/lemur-clusts/'):
	st.lemur2csv('/scratch/DSL/sincere-big-server/cnnfox/lemur-clusts/'+f,'/scratch/DSL/sincere-big-server/cnnfox/lemur-clusts-csv/'+f+'.csv')

#batch convert csv -> frequency, i.e. cllusterID -> frequency(doc count)
import os
import sys
sys.path.append('/proj/DSL/sincere/big-server/cnnfox/')
import soctoc as st

for f in os.listdir('/scratch/DSL/sincere-big-server/cnnfox/lemur-clusts-csv/'):
	infile='/scratch/DSL/sincere-big-server/cnnfox/lemur-clusts-csv/'+f
	outfile='.'.join(f.split('.')[0:-1]+['freq.csv']) #remove the trailing .csv from infile
	outfile='/scratch/DSL/sincere-big-server/cnnfox/lemur-clusts-freq/'+outfile
	g=st.dictbygroup(st.loadcsv(infile));st.savecsv({c:len(a) for c,a in g.items()},outfile)

#use functions in soctoc.py
infile='/tmp/cnn-comm.csv'
outfile='/tmp/soclust-count.csv'
g=st.dictbygroup(st.loadcsv(infile));st.savecsv({c:len(a) for c,a in g.items()},outfile)

#snap
 ./agmfitmain -i:/mnt/large/cnnfox/CNN-comment-edge.csv -l:/mnt/large/cnnfox/CNN-comment-label.csv -o:cnn


##gnuplot
plot '/tmp/lemur-148.csv' using 2:(1) smooth frequency with boxes
plot '/tmp/toclust-count-148.csv' using 2:(1) smooth frequency with boxes


