#CNN 5550296508

#Get length(in days) and number of comments in each post for CNN page
SELECT '#postid','duration','comment_count'
UNION ALL
SELECT post_id,TIMESTAMPDIFF(DAY,min(created_time),max(created_time)) AS duration, count(*) AS size
FROM comment
WHERE page_id=5550296508
GROUP BY post_id
INTO OUTFILE '/tmp/cnn_comment_duration_size.csv';

SELECT CONCAT('p',post_id), CONCAT('u',fb_id), YEARWEEK(DATE(created_time))
FROM comment
WHERE page_id=5550296508
INTO OUTFILE '/tmp/cnn_comment_yearweek.ncol';

