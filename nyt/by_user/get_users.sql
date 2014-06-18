SELECT DISTINCT c.fb_id, COUNT( DISTINCT c.post_id)
FROM comment c JOIN post p ON c.post_id=p.id
WHERE YEAR(p.created_time)=2012
GROUP BY fb_id;

UNION 
SELECT DISTINCT fb_id, post_id
FROM likedby 

###

SELECT CONCAT("u",c.fb_id),CONCAT("p",c.post_id) 
FROM
	(SELECT DISTINCT c.fb_id, c.post_id
	FROM comment c 
	WHERE YEARWEEK(created_time)=201251 
	) AS c 
	JOIN
	(SELECT fb_id
	FROM comment 
	WHERE YEARWEEK(created_time)=201251
	GROUP BY fb_id
	HAVING COUNT( DISTINCT post_id) > 5
	) AS u
	ON c.fb_id=u.fb_id


SELECT DISTINCT CONCAT("u",c.fb_id),CONCAT("p",c.post_id) 
FROM comment AS c JOIN (SELECT post_id,comment_id, COUNT(*) as likecount FROM likedby WHERE post_id IN (SELECT id FROM post WHERE  YEARWEEK(created_time)=201253) 
GROUP BY post_id,comment_id HAVING likecount > 1) 
AS l ON c.post_id=l.post_id AND c.id=l.comment_id;


