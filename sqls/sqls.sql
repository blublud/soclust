#CNN 5550296508

CREATE TABLE cnncomm (
	fbid BIGINT(20) PRIMARY KEY,
	ispost BOOLEAN,
	comm INT, 
	message TEXT, 
	url TEXT,
	fultext TEXT
);

# cp /scratch/DSL/sincere-big-server/cnnfox/cnn-comm.csv /tmp
# b/c mysql cannot load from /scratch/xxx

LOAD DATA INFILE '/tmp/cnn-comm.csv' 
INTO TABLE cnncomm(fbid,comm);

UPDATE cnncomm c JOIN post p ON c.fbid = p.id
SET c.ispost=TRUE, c.message=p.message;

UPDATE cnncomm 
SET ispost=FALSE
WHERE ispost is NULL;

UPDATE cnncomm
SET message=REPLACE(message,"\r","");

UPDATE cnncomm
SET message=REPLACE(message,"\n",".");

SELECT * FROM cnncomm
INTO OUTFILE '/tmp/cnn-comm-ispost-msg.csv';

INSERT INTO cnncomm(fbid,message)
	SELECT id, message from post
	WHERE page_id='5550296508'

#Get length(in days) and number of comments in each post for CNN page
SELECT '#postid','duration','comment_count'
UNION ALL
SELECT post_id,TIMESTAMPDIFF(DAY,min(created_time),max(created_time)) AS duration, count(*) AS size
FROM comment
WHERE page_id=5550296508
GROUP BY post_id
INTO OUTFILE '/tmp/cnn_comment_duration_size.csv';

#Get comment edges by yearweek
SELECT CONCAT('p',post_id), CONCAT('u',fb_id), YEARWEEK(DATE(created_time))
FROM comment
WHERE page_id=5550296508
INTO OUTFILE '/tmp/cnn_comment_yearweek.ncol';

CREATE TABLE yearweek(post BIGINT(20), usr BIGINT(20),yearweek INTEGER);
INSERT INTO yearweek(post,usr,yearweek)
SELECT CONCAT('p',post_id), CONCAT('u',fb_id), YEARWEEK(DATE(created_time))
FROM comment
WHERE page_id=5550296508;

#Get post in which entropy is dropped
DROP TABLE IF EXISTS temp_post;
CREATE TABLE temp_post like post;
DELETE FROM temp_post;
INSERT INTO temp_post 
	SELECT post.* 
	FROM post JOIN (SELECT DISTINCT(post_id) AS pid FROM comment WHERE YEARWEEK(DATE(created_time)) IN ('200934', '200930', '201203', '201202', '200922', '200921', '200925', '200924', '201042', '201038', '200948', '200941', '201245', '201012', '201013', '201015', '201243', '201002', '201001', '201304', '201247', '201246', '201301', '200912', '200910', '200916', '200915', '201244', '201303', '200909', '201216')) pid 
			ON post.id = pid.pid
;
UPDATE temp_post SET message=REPLACE(message,"\r","");
UPDATE temp_post SET message=REPLACE(message,"\n",".");
UPDATE temp_post SET message=REPLACE(message,"\t"," ");
UPDATE temp_post SET message='' WHERE message is NULL;

SELECT * FROM
(
	SELECT '#post_id', 'message'
	UNION ALL
	(SELECT CONCAT('p',id), message
	FROM temp_post)
) drop_entropy_message
INTO OUTFILE '/tmp/soclust/cnn_dropentropy_message.csv' FIELDS TERMINATED BY "\t" LINES TERMINATED BY "\n";
DROP TABLE temp_post;

