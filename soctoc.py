import csv
from collections import defaultdict
from math import log
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

'''
write content of dict d {k->v} to file
'''
def savecsv(d, csv_file):
	with open(csv_file,'w') as f:
		wtr=csv.writer(f,delimiter="\t")
		for k,v in d.items():
			wtr.writerow([k,v])
	
'''
Given file of lemur clustering result,  
read this file and output to csv entity_id;group_id
'''
def lemur2csv(lemurfile, csvfile):
	lemur=loadlemur(lemurfile)
	csv=open(csvfile,'w')
	for e,g in lemur.items():
		csv.write(e+"\t"+g+"\n")
	csv.close()

'''
soclust (stored in csvfile) consists both people and post
remove all entities in soclust that are not in lemur file
'''
def cleanup_soclust(lemur, soclust, outsoclust):
	l=loadcsv(lemur)
	s=loadcsv(soclust)
	outsoc={ e:g for e,g in s.items() if e in l}
	f=open(outsoclust,'w')
	for e,g in outsoc.items():
		f.write(e+"\t"+g+"\n")
	f.close()


#############################################
#IO FUNCTIONS
#############################################
'''
given a dictionary key=entity, val=group
build hash: {group_id->[entity_id]}
'''
def dictbygroup(ent_dict):
	d={}
	for ent,grp in ent_dict.items():
		if grp in d: d[grp].append(ent)
		else: d[grp]=[ent]
	return d
			
'''
given a list of entities (members) 
and classification of these entities
calculate the entropy value of this list.

members: a list o entities
classified: {entityId->groupId}
'''
def getentropy(members, classified):
	
	groups=defaultdict(lambda: 0)
	absence=0
	for e in members:
		if e in classified:
			groups[classified[e]]+=1
		else:
			absence+=1
	entropy=0.0
	size=len(members)-absence
	for g in groups:
		p=float(groups[g])/size
		entropy+= -(p)*log(p,2)
	return entropy

'''
given groups of entities,i.e. {groupid->[entities]}
and classification of those entities, i.e. classified{entityid -> classified}

calculate the entropies of each group.
'''
def getentropies(groups, classified):
	entropies = {gid:getentropy(members, classified) for gid,members in groups.items()}
	return entropies



