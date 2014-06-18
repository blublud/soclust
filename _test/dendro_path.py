#!/bin/python

def dendro_path(dendro_tree):
	'''
	Parse the scipy dendro_tree to get the full paths of each leaf in dendro tree.
	Parameters:
	dendro_tree: of type ClusterNode (scipy)
	Return:
	dict of {leaf_id:"path of 0_1_.."}
	'''
	leaves={}
	stack=[]
	trace=[]
	cur_pos='1'#a=left;b=right
	cur_node=dendro_tree
	last_visit=None
	
	while len(stack) or cur_node is not None:
		if cur_node is not None:
			stack.append(cur_node)
			trace.append(cur_pos)
			cur_pos='1'
			cur_node=cur_node.left
		else:
			peek=stack[-1]
			if peek.right is not None and last_visit != peek.right:
				cur_node=peek.right
				cur_pos='2'
			else:
				if (peek.left is None) and (peek.right is None):
					leaves[peek.id]=''.join([str(t) for t in trace])
				last_visit=stack.pop()
				trace.pop()
	max_len=max([len(trace) for trace in leaves.values()])
	for i,trace in leaves.items():
		leaves[i]=leaves[i].ljust(max_len,'0')
	return leaves

