#build weighted graph 
#CNN 5550296508

SELECT CONCAT('p',post_id), CONCAT('u',fb_id)
FROM cnnfox.comment
WHERE page_id=5550296508
INTO OUTFILE '/tmp/cnn.csv'
