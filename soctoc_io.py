
import csv
import re
'''
given lemur outputfile,
translate lemur's format to hash:{entityid->group}
'''
def loadlemur(lemurfile):
	f=open(lemurfile,'r')
	reg=re.compile('^(\d+)\(\d+\):')
				   

	res={}
	for l in f:
		m=reg.match(l)
		if not m: continue
		groupid=m.group(1)
		l=l[m.end():]
		res.update({e:groupid for e in l.split()})
	
	return res
	
'''
given a csv file: entity_id;group_id
build hash: {entity_id->group_id}
'''
def loadcsv(csv_file):

	with open(csv_file) as f:
		rdr = csv.reader(f,delimiter="\t")
		d={row[0].strip():row[1] for row in rdr}
		return d
