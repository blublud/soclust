#!/bin/bash

#setup lemur
sudo mkdir -p /mnt/large/cnnfox
sudo chmod a+rwx /mnt/large/cnnfox
sudo cp  /scratch/DSL/sincere-big-server/cnnfox/lemur-4.12.tar.gz /mnt/large/cnnfox
sudo tar -xzvf /scratch/DSL/sincere-big-server/cnnfox/lemur-4.12.tar.gz -C /mnt/large/cnnfox
sudo mv  /mnt/large/cnnfox/lemur-4.12 /mnt/large/cnnfox/lemur
sudo cp /proj/DSL/sincere/big-server/cnnfox/OfflineCluster.cpp /mnt/large/cnnfox/lemur/app/src/
cd /mnt/large/cnnfox/lemur/
sudo /mnt/large/cnnfox/lemur/configure --prefix=/mnt/large/cnnfox/lemur/ --enable-cluster --enable-java
sudo make
sudo make install

#sklearn
sudo apt-get install python-joblib
sudo apt-get install -y python-sklearn
#misc
sudo apt-get install python-mysqldb

