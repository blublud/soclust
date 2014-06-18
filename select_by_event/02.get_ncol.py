import csv
import os

f_postid_eventid='/tmp/nyt/postid_eventid.csv'
f_ncol='/tmp/nyt/ncol.ncol'
f_post_message='/tmp/nyt/postid_message.csv'
posts={}
with open(f_postid_eventid,'r') as f:
	rdr=csv.reader(f,delimiter='\t')
	for row in rdr:
		posts[row[0]]=row[1]

events={}
for p,e in posts.items():
	events[e]=1

print [p[1:] for p in posts.keys()]
print '# of events',len(events)

str_postids=','.join([p[1:] for p in posts.keys()])
os.system('sudo rm -f %s'%f_ncol)
os.system('sudo mysql -u root -ptoor nyt -e \'SELECT CONCAT("u",fb_id),CONCAT("p",post_id) FROM comment where post_id in (%s) INTO OUTFILE "%s";\''%(str_postids,f_ncol) )
os.system('sudo rm -f %s'%f_post_message)
os.system('sudo mysql -u root -ptoor nyt -e \'SELECT CONCAT("p",id),message FROM temp_post WHERE id in (%s) INTO OUTFILE "%s";\''%(str_postids,f_post_message))
