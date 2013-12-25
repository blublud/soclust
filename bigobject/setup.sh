#!/bin/bash
sudo apt-get update
sudo apt-get install -y python-software-properties
sudo add-apt-repository -y ppa:igraph/ppa
sudo apt-get update

sudo apt-get install -y python-igraph

wget http://mirrors.kernel.org/ubuntu/pool/universe/p/python-concurrent.futures/python-concurrent.futures_2.1.2-1_all.deb
sudo apt-get install python-support
sudo dpkg -i python-concurrent.futures_2.1.2-1_all.deb

mkdir -p /tmp/socgraph/
cd /tmp/socgraph/

wget https://dl.dropboxusercontent.com/u/38362652/cnn_comment_yearweek.ncol.tar.gz

tar -xzvf cnn_comment_yearweek.ncol.tar.gz

mkdir /tmp/socgraph/output/

