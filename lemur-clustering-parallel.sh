#!/bin/bash

sudo mkdir -p /tmp/cnnfox/
sudo chmod a+rwx /tmp/cnnfox/ 
cd /tmp/cnnfox/
sudo /mnt/large/cnnfox/lemur/app/obj/BuildIndex /proj/DSL/sincere/big-server/cnnfox/lemur-index-param.xml /scratch/DSL/sincere-big-server/cnnfox/cnn-message-only.trec

sudo python3 /proj/DSL/sincere/big-server/cnnfox/lemur-parallel-clustering.py
