##Works for RHEL/CentOS 6

#Get the CM repo
wget https://archive.cloudera.com/cm5/redhat/6/x86_64/cm/cloudera-manager.repo
#Copy the repo to repo dir
cp cloudera-manager.repo /etc/yum.repos.d/
#Install Oracle Java
sudo yum -y install oracle-j2sdk1.7
#Install CM embedded DB (which also installs CM server and CM daemon dependencies
sudo yum -y install cloudera-manager-server-db-2
#Start embedded DB
sudo service cloudera-scm-server-db start
#Start CM server
sudo service cloudera-scm-server start



