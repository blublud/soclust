#!/bin/bash
#setup emulab ubuntu server as remote desktop server
sudo apt-get install -y ubuntu-desktop
sudo apt-get install -y tightvncserver

sudo apt-get install -y xrdp
#create .xsession file with the content:x
sudo cp /proj/DSL/sincere/big-server/_gited/soclust/setup/.xsession /users/blublud/
sudo /etc/init.d/xrdp restart

sudo apt-get install -y firefox
#open terminal from rdp client; CTRL+ALT+T

#setup gephi
sudo mkdir -p /usr/lib/jvm/
sudo tar -xzvf /scratch/DSL/sincere-big-server/cnnfox/setup/jdk-7u45-linux-x64.tar-1.gz -C /usr/lib/jvm/
sudo update-alternatives --install "/usr/bin/java" "java" "/usr/lib/jvm/jdk1.7.0_45/bin/java" 1
sudo update-alternatives --install "/usr/bin/javac" "javac" "/usr/lib/jvm/jdk1.7.0_45/bin/javac" 1
sudo update-alternatives --install "/usr/bin/javaws" "javaws" "/usr/lib/jvm/jdk1.7.0_45/bin/javaws" 1

sudo mkdir -p /mnt/large/gephi/
sudo tar -xzvf /scratch/DSL/sincere-big-server/cnnfox/setup/gephi-0.8.2-beta.tar.gz -C /mnt/large
sudo update-alternatives --install "/usr/bin/gephi" "gephi" "/mnt/large/gephi/bin/gephi" 1

#install gephi's graph library
sudo apt-get install python-setuptools
sudo easy_install pip
sudo apt-get install -y python-dev
sudo apt-get install -y libxml2-dev
sudo pip install lxml
sudo pip install pygexf
#in python, use:'import gexf'


