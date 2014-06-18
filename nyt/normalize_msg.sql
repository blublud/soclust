DROP TABLE IF EXISTS temp_post;
CREATE TABLE temp_post like post;
INSERT INTO temp_post 
	SELECT * FROM post;
	
UPDATE temp_post SET message=REPLACE(message,"\r","");
UPDATE temp_post SET message=REPLACE(message,"\n",".");
UPDATE temp_post SET message=REPLACE(message,"\t"," ");
