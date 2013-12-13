#!/bin/bash

sudo stop mysql
sudo /proj/DSL/sincere/big-server/scriptlib/restore.sh /scratch/DSL/sincere-big-server/cnnfox/ / cnnfox-db
sudo /proj/DSL/sincere/big-server/scriptlib/copy-retry.sh /scratch/DSL/sincere-big-server/db-backup/ibdata1 /var/lib/mysql/
sudo /proj/DSL/sincere/big-server/scriptlib/copy-retry.sh /scratch/DSL/sincere-big-server/db-backup/ib_logfile0 /var/lib/mysql/
sudo /proj/DSL/sincere/big-server/scriptlib/copy-retry.sh /scratch/DSL/sincere-big-server/db-backup/ib_logfile1 /var/lib/mysql/
sudo start mysql
