from concurrent import futures

def work(arg):
	(c,a)=arg
	print c
	print a

args=((i, [i]*3) for i in range(5))

with futures.ProcessPoolExecutor(max_workers=32) as executor:
	for i in executor.map(work, args):
		pass
