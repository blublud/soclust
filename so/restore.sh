#!/bin/bash

sudo mkdir -p /tmp/289/data/
sudo chmod a+rwx /tmp/289/data/
for file in /scratch/DSL/sincere-big-server/289/data/*
do
	res=1
	while [[ res -ne 0 ]]
	do
		sudo cp -v "$file" /tmp/289/data
		res=$?
	done
done

sudo cat /tmp/289/data/stackoverflow.com-Posts* > /tmp/289/data/stackoverflow.com-Posts.7z
sudo cat /tmp/289/data/stackoverflow.com-Users* > /tmp/289/data/stackoverflow.com-Users.7z
sudo cat /tmp/289/data/stackoverflow.com-Votes* > /tmp/289/data/stackoverflow.com-Votes.7z

sudo apt-get install p7zip-full

cd /tmp/289/data/
sudo 7z x "*.7z"

sudo start mysql
sudo mysql -u root -ptoor -e 'DROP DATABASE IF EXISTS so;'
sudo mysql -u root -ptoor -e 'CREATE DATABASE so;'

sudo mysql --local-infile -u root -ptoor so -e 'CREATE TABLE users( Id INT, Reputation INT, RepuRank FLOAT, CreationDate DATETIME, DisplayName NVARCHAR(40), LastAccessDate DATETIME, WebsiteUrl NVARCHAR(200), Location NVARCHAR(100), AboutMe NVARCHAR(65532), Views INT, UpVotes INT, DownVotes INT, ProfileImageUrl NVARCHAR(20),EmailHash VARCHAR(20),Age INT,AccountId INT, INDEX(Id) );LOAD XML LOCAL INFILE "/tmp/289/data/stackoverflow.com-Users"  INTO TABLE users(Id, Reputation, CreationDate,DisplayName, LastAccessDate, WebsiteUrl, Location, AboutMe, Views, UpVotes, DownVotes, AccountId );'
 
sudo mysql --local-infile -u root -ptoor so -e 'CREATE TABLE votes(Id INT, PostId INT, VoteTypeId TINYINT,UserId INT,CreationDate DATETIME,BountyAmount INT, INDEX(Id,PostId));LOAD XML LOCAL INFILE "/tmp/289/data/stackoverflow.com-Votes"  INTO TABLE votes; '

sudo mysql --local-infile -u root -ptoor so -e 'CREATE TABLE posts(Id INT, PostTypeId TINYINT, AcceptedAnswerId INT, ParentId INT, CreationDate DATETIME, Score INT, ViewCount INT, Body NVARCHAR(65532), OwnerUserId INT, LastEditorUserId INT,LastEditDate DATETIME,LastActivityDate DATETIME,AnswerCount INT,CommentCount INT,FavoriteCount INT,ClosedDate DATETIME,CommunityOwnedDate DATETIME, Tags NVARCHAR(150), INDEX(Id,PostTypeId,OwnerUserId));LOAD XML LOCAL INFILE "/tmp/289/data/stackoverflow.com-Posts" INTO TABLE posts;'

sudo mysql --local-infile -u root -ptoor so -e 'CREATE TABLE posthistory(Id INT, PostHistoryTypeId TINYINT, PostId INT, RevisionGUID CHAR(38), CreationDate DATETIME, UserId INT, INDEX(Id, PostId, UserId));LOAD XML LOCAL INFILE "/tmp/289/data/stackoverflow.com-PostHistory"  INTO TABLE posthistory(Id, PostHistoryTypeId, PostId, RevisionGUID, CreationDate, UserId); '

sudo mysql --local-infile -u root -ptoor so -e 'CREATE TABLE Badges(Id int,UserId int,Name NVARCHAR(50),Date datetime, INDEX(Id,UserId,Name));LOAD XML LOCAL INFILE "/tmp/289/data/stackoverflow.com-Badges" INTO TABLE Badges(Id,UserId,Name,Date);'

echo "*DONE RESTORING 289*"

