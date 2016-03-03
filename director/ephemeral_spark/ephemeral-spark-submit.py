#-*- coding: utf-8 -*-
import argparse, cluster, ConfigParser, sys, subprocess
from cloudera.director.common.client import ApiClient
from cloudera.director.latest import AuthenticationApi, EnvironmentsApi
from cloudera.director.latest.models import Login
from cloudera.director.latest import ClustersApi
from cloudera.director.latest.models import Cluster
from cloudera.director.latest.models import Instance
from os.path import isfile
from urllib2 import HTTPError

#Copies JAR to the gateway
def copy_jar(jar,gateway,config):
    username = config.get("ssh", "username")
    key = config.get("ssh", "privateKey")
    connect_string = username + '@' + gateway + ':/home/' + username
    print('Copying jar ' + jar  + ' to ' + connect_string + ' using the key located at ' + key)   
    p = subprocess.Popen(['scp','-i',key,'-o',"StrictHostKeyChecking=no",jar,connect_string],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = p.communicate()
    if err:
        print(err)
        return 1
    else:
        print(out)
        return 0

#Copies script to the gateway
def copy_script(script,gateway,config):
    username = config.get("ssh", "username")
    key = config.get("ssh", "privateKey")
    connect_string = username + '@' + gateway + ':/home/' + username 
    print('Copying script ' + script  + ' to ' + connect_string + ' using the key located at ' + key)
    p = subprocess.Popen(['scp','-i',key,'-o',"StrictHostKeyChecking=no",script,connect_string],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = p.communicate()
    if err:
        print(err)
        return 1
    else:
        print(out)
        return 0
#Creates HDFS directory owned by your user on HDFS
def configure_hdfs(gateway,config):
    username = config.get("ssh", "username")
    key = config.get("ssh", "privateKey")
    connect_string = username + '@' + gateway
    hdfs_commands = 'sudo -u hdfs hdfs dfs -mkdir /user/' + username + ' ; sudo -u hdfs hdfs dfs -chown ' + username + ':' + username + ' /user/' + username + ' ; exit'
    print('Creating an HDFS directory for user ' + username + ' on the ephemeral cluster')
    p = subprocess.Popen(['ssh','-tt','-i',key,'-o',"StrictHostKeyChecking=no",connect_string,hdfs_commands],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = p.communicate()
    if err:
        print(err)
        return 1
    else:
        print(out)
        return 0

#Executes script
def execute_script(script,gateway,config):
    username = config.get("ssh", "username")
    key = config.get("ssh", "privateKey")
    connect_string = username + '@' + gateway
    script_commands = 'chmod +x ' + script + ' ; ./' + script
    print('Running script on ephemeral scluster')
    p = subprocess.Popen(['ssh','-i',key,'-o',"StrictHostKeyChecking=no",connect_string,script_commands],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = p.communicate()
    if err:
        print(err)
        return 1
    else:
        print(out)
        return 0
#Execute Spark job on cluster
def execute_spark(jar,jarclass,args,gateway,config):
    username = config.get("ssh", "username")
    key = config.get("ssh", "privateKey")
    connect_string = username + '@' + gateway
    spark_commands = 'cd /home/' + username + ' ; spark-submit --class ' + jarclass + ' --deploy-mode client --master yarn ' + jar + ' ' + args
    print('Executing Spark job on the ephemeral cluster:')
    p = subprocess.Popen(['ssh','-i',key,'-o',"StrictHostKeyChecking=no",connect_string,spark_commands],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = p.communicate()
    if err:
        print(err)
        return 1
    else:
        print(out)
        return 0

def main():
    parser = argparse.ArgumentParser(prog='ephemeral-spark-submit.py')
    parser.add_argument('--admin-username', default="admin",
                        help='Name of an user with administrative access (defaults to %(default)s)')
    parser.add_argument('--admin-password', default="admin",
                        help='Password for the administrative user (defaults to %(default)s)')
    parser.add_argument('--server', default="http://localhost:7189",
                        help="Cloudera Director server URL (defaults to %(default)s)")
    parser.add_argument('--cm', help="The name of the Cloudera Manager server to use in Director")
    parser.add_argument('--environment', help="The name of the Environment to use in Director")
    parser.add_argument('--jar',help="JAR for Spark job you want to run on ephemeral cluster")
    parser.add_argument('--jarclass',help="The --class flag for spark-submit")
    parser.add_argument('--args',help="The arguments for the jar")
    parser.add_argument('--script',help="Script that runs before spark job")
    parser.add_argument('config_file', help="Cluster configuration file (.ini)")
    args = parser.parse_args() 

    if not isfile(args.config_file):
        print 'Error: "%s" not found or not a file' % args.config_file
        return -1

    config = ConfigParser.SafeConfigParser()
    config.read(args.config_file) 
    
    #Create authenticated client 
    client = cluster.get_authenticated_client(args)
    
    #Execute cluster creation
    cluster_name = cluster.create_cluster(client, args.environment, args.cm, config)
    print 'Waiting for the cluster to be ready. Check the web interface for details.'
    cluster.wait_for_cluster(client, args.environment, args.cm, cluster_name)
    client = ApiClient(args.server)
    AuthenticationApi(client).login(Login(username="admin", password="admin"))
    clusters = ClustersApi(client)
    eph_cluster = clusters.get(args.environment,args.cm,cluster_name)
    instances = eph_cluster.instances
    #Find which is a gateway node
    for instance in instances:
        if str(instance.virtualInstance.template.name) == 'gateway':
            gateway = instance
    gateway = gateway.properties['publicDnsName']
    print("The Gateway url is: " + gateway)
    
    #Copy the JAR and postscript to the GW
    copy_jar(args.jar,gateway,config)
    #Copy script to the GW
    copy_script(args.script,gateway,config)
    #Create directory in HDFS with correct permissions
    configure_hdfs(gateway,config)
    #Execute the job
    execute_spark(args.jar,args.jarclass,args.args,gateway,config)
    #Run some post script
    execute_script(args.script,gateway,config)
    #Destroy the cluster
    print "Job complete, terminating the instance"
    clusters.delete(args.environment,args.cm,cluster_name)

    

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())

    except HTTPError as e:
        print e.read()
        raise e
