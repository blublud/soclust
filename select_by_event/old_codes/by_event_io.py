import csv
import MySQLdb
import argparse

'''
ENVIRONMENT SETUP:
sudo apt-get install python-mysqldb
'''

db=MySQLdb.connect(host='localhost',user='root',passwd='toor',db='nyt')
cur=db.cursor()

#cnn 5550296508
#SELECT_BY_EVENT_KEYWORD='SELECT id FROM post WHERE page_id=\'5550296508\' AND %s AND created_time BETWEEN %s - INTERVAL 10 DAY AND %s + INTERVAL 30 DAY;'
#fox:15704546335
#SELECT_BY_EVENT_KEYWORD='SELECT id FROM post WHERE page_id=\'15704546335\' AND %s AND created_time BETWEEN %s - INTERVAL 10 DAY AND %s + INTERVAL 30 DAY;'
#nyt:5281959998
SELECT_BY_EVENT_KEYWORD='SELECT id FROM post WHERE page_id=\'5281959998\' AND %s AND created_time BETWEEN %s - INTERVAL 10 DAY AND %s + INTERVAL 30 DAY;'

def main():

	parser=argparse.ArgumentParser()
	parser.add_argument("input_file",help="Input csv file listing all events and derived keywords")
	parser.add_argument("output_file",help="Output csv file (post_id, event_id")
	args=parser.parse_args()
	f_input=args.input_file
	f_output=args.output_file

	posts_by_event=select_post_from_file(f_input)
	postid_eventid=get_postid_eventid(posts_by_event)
	save_postid_event(postid_eventid,f_output)

def select_posts(keywords,event_date):
	keyword_predicate=' AND '.join(['message LIKE \'%'+kw+'%\'' for kw in keywords])
	start_date='\'%s/%s/%s\''%event_date

	query=SELECT_BY_EVENT_KEYWORD%(keyword_predicate,start_date,start_date)
	postIds=[]
	cur.execute(query)
	for row in cur.fetchall():
		postIds.append('p'+str(row[0]))
	return postIds	

def select_post_from_file(f_name):
	posts_by_event=[]
	with open(f_name,'rb') as f:
		r=csv.reader(f,delimiter='\t',quotechar=None)
		for row in [row for row in r if len(row) and not row[0].startswith('#')]:
			event_date=(row[0],row[1],row[2])
			keywords=row[4].split(';')
			summary=row[3]
			postIds=select_posts(keywords,event_date)
			posts_by_event.append((event_date,summary,keywords,postIds))
	return posts_by_event

def save_posts_by_event(posts_by_event,f_name):
	with open(f_name,'wb') as f:
		w=csv.writer(f,delimiter='\t',quotechar=None)
		for i,postDetails in enumerate(posts_by_event):
			((yy,mm,dd),summary,keywords,postIds)=postDetails
			w.writerow([i,yy,mm,dd,summary,';'.join(keywords),';'.join([str(p) for p in postIds])] )

def get_postid_eventid(posts_by_event):
	postid_event={}
	for eventId,eventDetails in enumerate(posts_by_event):
		(_1,_2,_3,postsIds)=eventDetails
		for postId in postsIds:
			if postId in postid_event:
				postid_event[postId].append(eventId)
			else:
				postid_event[postId]=[eventId]
	return postid_event

def save_postid_event(posts_by_event,f_name):

	with open(f_name,'wb') as f:
		w=csv.writer(f,delimiter='\t',quotechar=None)
		for postId,eventsIds in posts_by_event.items():
			w.writerow([str(postId),';'.join([str(eventId) for eventId in eventsIds])])

def load_postid_eventid(f_name):
	posts_by_event={}
	with open(f_name,'rb') as f:
		r=csv.reader(f,delimiter='\t',quotechar=None)
		for row in [row for row in r if len(row) and not row[0].startswith('#')]:
			postid=row[0]
			eventsIds=row[1]

	return posts_by_event
	
if __name__=='__main__':
	main()
