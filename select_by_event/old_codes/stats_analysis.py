from collections import defaultdict
from math import log
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
	for memCount in (memCount for _,memCount in groups.items() if memCount):		
		p=float(memCount)/size
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


'''
Calculate the entropies of elements in each class in classified1. to see how it is distributed in classified2
for each class in classified1, calculate its elements distribution in classified 2.
Input:
	classified1=classified2={element->class}
'''
def entropies(classified1,classified2):

	dict_classes1=defaultdict(lambda: [])
	for e,class1 in classified1.items():
		dict_classes1[class1].append(e)

	return getentropies(dict_classes1,classified2)
