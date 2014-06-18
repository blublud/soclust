#SELECT Id,TagName,ISNULL(Count,-1) AS Count, ISNULL(ExcerptPostId,-1) AS ExcerptPostId, ISNULL(WikiPostId,-1) AS WikiPostId FROM Tags;

sudo mkdir -p /tmp/289
cd /tmp/289/

sudo apt-get install p7zip-full
sudo apt-get install python-mysqldb
sudo apt-get install -y python-tk
sudo apt-get install -y python-matplotlib

sudo apt-get install -y python-setuptools
sudo apt-get install -y python-dev

#sudo easy_install pandas
#sudo easy_install patsy
#sudo easy_install statsmodels

#sudo git clone git://github.com/statsmodels/statsmodels.git
#cd statsmodels
#sudo python setup.py build
#sudo python setup.py install
#cd ..

