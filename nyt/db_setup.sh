#/bin/bash
sudo mysql -u root -ptoor -e 'DROP DATABASE IF EXISTS nyt;'
sudo mysql -u root -ptoor -e 'CREATE DATABASE nyt;'
sudo mysql -u root -ptoor -e 'CREATE TABLE nyt.post LIKE sincere.post;'
sudo mysql -u root -ptoor -e 'CREATE TABLE nyt.comment LIKE sincere.comment;'
sudo mysql -u root -ptoor -e 'CREATE TABLE nyt.likedby LIKE sincere.likedby;'
sudo mysql -u root -ptoor -e 'CREATE TABLE nyt.fb_user LIKE sincere.fb_user;'

sudo mysql -u root -ptoor -e 'INSERT INTO nyt.post (SELECT * FROM sincere.post WHERE page_id=5281959998);'
sudo mysql -u root -ptoor -e 'INSERT INTO nyt.comment (SELECT * FROM sincere.comment WHERE page_id=5281959998);'
sudo mysql -u root -ptoor -e 'INSERT INTO nyt.likedby (SELECT * FROM sincere.likedby WHERE page_id=5281959998);'
