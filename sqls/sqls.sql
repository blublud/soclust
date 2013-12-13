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
