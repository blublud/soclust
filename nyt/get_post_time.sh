#!/bin/bash
sudo mysql -u root -ptoor nyt -e 'SELECT CONCAT("p",id), created_time FROM temp_post WHERE YEARWEEK(created_time)=201253 INTO OUTFILE "/tmp/nyt/post_time_201253.csv" FIELDS TERMINATED BY "\t";'
