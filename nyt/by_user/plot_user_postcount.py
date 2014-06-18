'''
Query # of post each user has interacted with
SELECT DISTINCT c.fb_id, COUNT( DISTINCT c.post_id)
FROM comment c JOIN post p ON c.post_id=p.id
WHERE YEAR(p.created_time)=2012
GROUP BY fb_id;
'''
q='SELECT DISTINCT c.fb_id, COUNT( DISTINCT c.post_id) FROM comment c JOIN post p ON c.post_id=p.id WHERE YEAR(p.created_time)=2012 GROUP BY fb_id;'

import matplotlib
matplotlib.use('Agg')

import MySQLdb
db=MySQLdb.connect(host='localhost',user='root',passwd='toor',db='nyt')

cur =db.cursor()
cur.execute(q)

data=[]
for row in cur.fetchall():
	data.append(row[1])

import matplotlib.pyplot as plt
plt.figure()
plt.hist(data,bins=50,log=True)
#plt.xscale('log')

plt.savefig('/scratch/DSL/sincere-big-server/tmp/postcount_per_user_2012.png')


