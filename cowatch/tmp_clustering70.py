import sys
import cPickle

sys.path.append('/proj/DSL/sincere/big-server/cnnfox/cowatch/')
from cowatch_graph import *

do_clustering(dendroFile='/tmp/cnn2-dendo-p-0.700000.dat', resultfile='/tmp/cnn2-clusts-p-0.7.clust')
