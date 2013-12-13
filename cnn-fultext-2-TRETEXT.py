import csv

get_message=0
get_fultext=1
with open('/scratch/DSL/sincere-big-server/cnnfox/cnn-comm-ispost-fultext.csv') as csvfile:
	rdr = csv.reader(csvfile,delimiter="\t")
		
	for row in rdr:		
		fbid=row[0]
		ispost=row[1]
		message=row[3]
		url=row[4]
		fultext=row[5]
		
		print_message = get_message and message != '\N'
		print_fultext = get_fultext and fultext!= '\N'

		if not (print_message or print_fultext): continue
		
		print "<DOC>"
		print "<DOCNO>",fbid,"</DOCNO>"
	
		if print_message:
			print message
		if print_fultext:
			print fultext
		
		print "</DOC>"

