####Ephemeral Spark Cluster Job Submission
Spin up a Spark cluster using Cloudera Director, submit a job, store output, destroy cluster. It should be noted that some of this code was borrowed from the python director client samples (most notably, cluster.py and cluster.ini). I have modified/added to it so that I could demonstrate a way to spin up transient clusters. 

###Getting started
Clone this repo:
```
git clone https://github.com/bkvarda/hadoop_stuff.git
```
Change into to correct directory:
```
cd hadoop_stuff/director/spark_ephemeral
```
Install the Cloudera Director Client (for Python)
```
pip install cloudera-director-python-client
```

Modify cluster.ini to include your instance/credential information, and modify the postscript to include your AWS/S3 information

Execute your spark job like this:
```
python ephemeral-spark-submit.py --admin-username admin --admin-password password --server http://your_director_instance.compute-1.amazonaws.com:7189 --cm CM01 --environment CDH5_5 --jar spark-pi.jar --jarclass org.apache.spark.examples.SparkPi --args "100 10" --script copy_results.sh cluster.ini
```
The script will then do the following:
* Spin up a cluster with 1 master, 1 gateway, and the number of data/spark nodes you quantified in your cluster.ini
* When the cluster is up, your JAR file is copied to the home directory of the user that created the cluster
* An HDFS directory is created for /user/username owned by that user
* The job is executed using spark-submit
* A postscript is then ran (in this example copying the entire user directory/output to S3)
* Deletes the cluster that was created

The full output should look like this if everything is entered correctly:
```
Clusters: ['Spark_ephemeral']
Waiting for the cluster to be ready. Check the web interface for details.
...........................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................
Cluster 'Spark_ephemeral' current stage is 'READY'
The Gateway url is: ec2-somewhere.compute-1.amazonaws.com
Copying jar spark-pi.jar to ec2-user@ec2-somewhere.compute-1.amazonaws.com:/home/ec2-user using the key located at awskey.pem
Warning: Permanently added 'ec2-somewhere.compute-1.amazonaws.com,52.201.237.231' (RSA) to the list of known hosts.

Copying script copy_results.sh to ec2-user@ec2-somewhere.compute-1.amazonaws.com:/home/ec2-user using the key located at awskey.pem

Creating an HDFS directory for user ec2-user on the ephemeral cluster
Connection to ec2-somewhere.compute-1.amazonaws.com closed.

Executing Spark job on the ephemeral cluster:
16/03/03 00:26:45 INFO SparkContext: Running Spark version 1.5.0-cdh5.5.2
16/03/03 00:26:46 INFO SecurityManager: Changing view acls to: ec2-user
16/03/03 00:26:46 INFO SecurityManager: Changing modify acls to: ec2-user
16/03/03 00:26:46 INFO SecurityManager: SecurityManager: authentication disabled; ui acls disabled; users with view permissions: Set(ec2-user); users with modify permissions: Set(ec2-user)
16/03/03 00:26:46 INFO Slf4jLogger: Slf4jLogger started
16/03/03 00:26:47 INFO Remoting: Starting remoting
16/03/03 00:26:47 INFO Remoting: Remoting started; listening on addresses :[akka.tcp://sparkDriver@10.0.0.60:55853]
16/03/03 00:26:47 INFO Remoting: Remoting now listens on addresses: [akka.tcp://sparkDriver@10.0.0.60:55853]
16/03/03 00:26:47 INFO Utils: Successfully started service 'sparkDriver' on port 55853.
16/03/03 00:26:47 INFO SparkEnv: Registering MapOutputTracker
16/03/03 00:26:47 INFO SparkEnv: Registering BlockManagerMaster
16/03/03 00:26:47 INFO DiskBlockManager: Created local directory at /tmp/blockmgr-2fa9eef1-aadc-4656-95b4-565268b97081
16/03/03 00:26:47 INFO MemoryStore: MemoryStore started with capacity 530.3 MB
16/03/03 00:26:47 INFO HttpFileServer: HTTP File server directory is /tmp/spark-07df4e2a-afc8-4687-b30d-21a7b2d49a14/httpd-40698a85-f085-47d4-92b9-66d322dfca33
16/03/03 00:26:47 INFO HttpServer: Starting HTTP Server
16/03/03 00:26:47 INFO Utils: Successfully started service 'HTTP file server' on port 59337.
16/03/03 00:26:48 INFO SparkEnv: Registering OutputCommitCoordinator
16/03/03 00:26:48 INFO Utils: Successfully started service 'SparkUI' on port 4040.
16/03/03 00:26:48 INFO SparkUI: Started SparkUI at http://10.0.0.60:4040
16/03/03 00:26:49 INFO SparkContext: Added JAR file:/home/ec2-user/spark-pi.jar at http://10.0.0.60:59337/jars/spark-pi.jar with timestamp 1456982809327
16/03/03 00:26:49 WARN MetricsSystem: Using default name DAGScheduler for source because spark.app.id is not set.
16/03/03 00:26:49 INFO RMProxy: Connecting to ResourceManager at ip-10-0-0-120.ec2.internal/10.0.0.120:8032
16/03/03 00:26:49 INFO Client: Requesting a new application from cluster with 3 NodeManagers
16/03/03 00:26:49 INFO Client: Verifying our application has not requested more than the maximum memory capability of the cluster (3029 MB per container)
16/03/03 00:26:49 INFO Client: Will allocate AM container, with 896 MB memory including 384 MB overhead
16/03/03 00:26:49 INFO Client: Setting up container launch context for our AM
16/03/03 00:26:49 INFO Client: Setting up the launch environment for our AM container
16/03/03 00:26:49 INFO Client: Preparing resources for our AM container
16/03/03 00:26:51 INFO Client: Uploading resource file:/tmp/spark-07df4e2a-afc8-4687-b30d-21a7b2d49a14/__spark_conf__1120800026656331726.zip -> hdfs://ip-10-0-0-120.ec2.internal:8020/user/ec2-user/.sparkStaging/application_1456982691678_0001/__spark_conf__1120800026656331726.zip
16/03/03 00:26:52 INFO SecurityManager: Changing view acls to: ec2-user
16/03/03 00:26:52 INFO SecurityManager: Changing modify acls to: ec2-user
16/03/03 00:26:52 INFO SecurityManager: SecurityManager: authentication disabled; ui acls disabled; users with view permissions: Set(ec2-user); users with modify permissions: Set(ec2-user)
16/03/03 00:26:52 INFO Client: Submitting application 1 to ResourceManager
16/03/03 00:26:52 INFO YarnClientImpl: Submitted application application_1456982691678_0001
16/03/03 00:26:53 INFO Client: Application report for application_1456982691678_0001 (state: ACCEPTED)
16/03/03 00:26:53 INFO Client:
	 client token: N/A
	 diagnostics: N/A
	 ApplicationMaster host: N/A
	 ApplicationMaster RPC port: -1
	 queue: root.ec2-user
	 start time: 1456982812325
	 final status: UNDEFINED
	 tracking URL: http://ip-10-0-0-120.ec2.internal:8088/proxy/application_1456982691678_0001/
	 user: ec2-user
16/03/03 00:26:54 INFO Client: Application report for application_1456982691678_0001 (state: ACCEPTED)
16/03/03 00:26:55 INFO Client: Application report for application_1456982691678_0001 (state: ACCEPTED)
16/03/03 00:26:56 INFO Client: Application report for application_1456982691678_0001 (state: ACCEPTED)
16/03/03 00:26:57 INFO Client: Application report for application_1456982691678_0001 (state: ACCEPTED)
16/03/03 00:26:58 INFO Client: Application report for application_1456982691678_0001 (state: ACCEPTED)
16/03/03 00:26:59 INFO YarnSchedulerBackend$YarnSchedulerEndpoint: ApplicationMaster registered as AkkaRpcEndpointRef(Actor[akka.tcp://sparkYarnAM@10.0.0.208:53457/user/YarnAM#1784829206])
16/03/03 00:26:59 INFO YarnClientSchedulerBackend: Add WebUI Filter. org.apache.hadoop.yarn.server.webproxy.amfilter.AmIpFilter, Map(PROXY_HOSTS -> ip-10-0-0-120.ec2.internal, PROXY_URI_BASES -> http://ip-10-0-0-120.ec2.internal:8088/proxy/application_1456982691678_0001), /proxy/application_1456982691678_0001
16/03/03 00:26:59 INFO JettyUtils: Adding filter: org.apache.hadoop.yarn.server.webproxy.amfilter.AmIpFilter
16/03/03 00:26:59 INFO Client: Application report for application_1456982691678_0001 (state: RUNNING)
16/03/03 00:26:59 INFO Client:
	 client token: N/A
	 diagnostics: N/A
	 ApplicationMaster host: 10.0.0.208
	 ApplicationMaster RPC port: 0
	 queue: root.ec2-user
	 start time: 1456982812325
	 final status: UNDEFINED
	 tracking URL: http://ip-10-0-0-120.ec2.internal:8088/proxy/application_1456982691678_0001/
	 user: ec2-user
16/03/03 00:26:59 INFO YarnClientSchedulerBackend: Application application_1456982691678_0001 has started running.
16/03/03 00:26:59 INFO Utils: Successfully started service 'org.apache.spark.network.netty.NettyBlockTransferService' on port 33939.
16/03/03 00:26:59 INFO NettyBlockTransferService: Server created on 33939
16/03/03 00:26:59 INFO BlockManager: external shuffle service port = 7337
16/03/03 00:26:59 INFO BlockManagerMaster: Trying to register BlockManager
16/03/03 00:26:59 INFO BlockManagerMasterEndpoint: Registering block manager 10.0.0.60:33939 with 530.3 MB RAM, BlockManagerId(driver, 10.0.0.60, 33939)
16/03/03 00:26:59 INFO BlockManagerMaster: Registered BlockManager
16/03/03 00:26:59 INFO EventLoggingListener: Logging events to hdfs://ip-10-0-0-120.ec2.internal:8020/user/spark/applicationHistory/application_1456982691678_0001
16/03/03 00:26:59 INFO YarnClientSchedulerBackend: SchedulerBackend is ready for scheduling beginning after reached minRegisteredResourcesRatio: 0.8
16/03/03 00:27:00 INFO SparkContext: Starting job: reduce at SparkPi.scala:36
16/03/03 00:27:00 INFO DAGScheduler: Got job 0 (reduce at SparkPi.scala:36) with 100 output partitions
16/03/03 00:27:00 INFO DAGScheduler: Final stage: ResultStage 0(reduce at SparkPi.scala:36)
16/03/03 00:27:00 INFO DAGScheduler: Parents of final stage: List()
16/03/03 00:27:00 INFO DAGScheduler: Missing parents: List()
16/03/03 00:27:00 INFO DAGScheduler: Submitting ResultStage 0 (MapPartitionsRDD[1] at map at SparkPi.scala:32), which has no missing parents
16/03/03 00:27:00 INFO MemoryStore: ensureFreeSpace(1888) called with curMem=0, maxMem=556038881
16/03/03 00:27:00 INFO MemoryStore: Block broadcast_0 stored as values in memory (estimated size 1888.0 B, free 530.3 MB)
16/03/03 00:27:00 INFO MemoryStore: ensureFreeSpace(1186) called with curMem=1888, maxMem=556038881
16/03/03 00:27:00 INFO MemoryStore: Block broadcast_0_piece0 stored as bytes in memory (estimated size 1186.0 B, free 530.3 MB)
16/03/03 00:27:00 INFO BlockManagerInfo: Added broadcast_0_piece0 in memory on 10.0.0.60:33939 (size: 1186.0 B, free: 530.3 MB)
16/03/03 00:27:00 INFO SparkContext: Created broadcast 0 from broadcast at DAGScheduler.scala:861
16/03/03 00:27:00 INFO DAGScheduler: Submitting 100 missing tasks from ResultStage 0 (MapPartitionsRDD[1] at map at SparkPi.scala:32)
16/03/03 00:27:00 INFO YarnScheduler: Adding task set 0.0 with 100 tasks
16/03/03 00:27:01 INFO ExecutorAllocationManager: Requesting 1 new executor because tasks are backlogged (new desired total will be 1)
16/03/03 00:27:02 INFO ExecutorAllocationManager: Requesting 2 new executors because tasks are backlogged (new desired total will be 3)
16/03/03 00:27:03 INFO ExecutorAllocationManager: Requesting 4 new executors because tasks are backlogged (new desired total will be 7)
16/03/03 00:27:04 INFO ExecutorAllocationManager: Requesting 8 new executors because tasks are backlogged (new desired total will be 15)
16/03/03 00:27:05 INFO ExecutorAllocationManager: Requesting 16 new executors because tasks are backlogged (new desired total will be 31)
16/03/03 00:27:06 INFO ExecutorAllocationManager: Requesting 32 new executors because tasks are backlogged (new desired total will be 63)
16/03/03 00:27:06 INFO YarnClientSchedulerBackend: Registered executor: AkkaRpcEndpointRef(Actor[akka.tcp://sparkExecutor@ip-10-0-0-206.ec2.internal:60905/user/Executor#1289138840]) with ID 1
16/03/03 00:27:06 INFO ExecutorAllocationManager: New executor 1 has registered (new total is 1)
16/03/03 00:27:07 INFO TaskSetManager: Starting task 0.0 in stage 0.0 (TID 0, ip-10-0-0-206.ec2.internal, partition 0,PROCESS_LOCAL, 2031 bytes)
16/03/03 00:27:07 INFO BlockManagerMasterEndpoint: Registering block manager ip-10-0-0-206.ec2.internal:43378 with 530.3 MB RAM, BlockManagerId(1, ip-10-0-0-206.ec2.internal, 43378)
16/03/03 00:27:07 INFO ExecutorAllocationManager: Requesting 37 new executors because tasks are backlogged (new desired total will be 100)
16/03/03 00:27:07 INFO YarnClientSchedulerBackend: Registered executor: AkkaRpcEndpointRef(Actor[akka.tcp://sparkExecutor@ip-10-0-0-208.ec2.internal:50472/user/Executor#-692194341]) with ID 3
16/03/03 00:27:07 INFO ExecutorAllocationManager: New executor 3 has registered (new total is 2)
16/03/03 00:27:07 INFO TaskSetManager: Starting task 1.0 in stage 0.0 (TID 1, ip-10-0-0-208.ec2.internal, partition 1,PROCESS_LOCAL, 2033 bytes)
16/03/03 00:27:07 INFO BlockManagerMasterEndpoint: Registering block manager ip-10-0-0-208.ec2.internal:58721 with 530.3 MB RAM, BlockManagerId(3, ip-10-0-0-208.ec2.internal, 58721)
16/03/03 00:27:08 INFO YarnClientSchedulerBackend: Registered executor: AkkaRpcEndpointRef(Actor[akka.tcp://sparkExecutor@ip-10-0-0-207.ec2.internal:41983/user/Executor#-1817839882]) with ID 2
16/03/03 00:27:08 INFO ExecutorAllocationManager: New executor 2 has registered (new total is 3)
16/03/03 00:27:08 INFO TaskSetManager: Starting task 2.0 in stage 0.0 (TID 2, ip-10-0-0-207.ec2.internal, partition 2,PROCESS_LOCAL, 2033 bytes)
16/03/03 00:27:08 INFO BlockManagerMasterEndpoint: Registering block manager ip-10-0-0-207.ec2.internal:60768 with 530.3 MB RAM, BlockManagerId(2, ip-10-0-0-207.ec2.internal, 60768)
16/03/03 00:27:08 INFO BlockManagerInfo: Added broadcast_0_piece0 in memory on ip-10-0-0-206.ec2.internal:43378 (size: 1186.0 B, free: 530.3 MB)
16/03/03 00:27:08 INFO TaskSetManager: Starting task 3.0 in stage 0.0 (TID 3, ip-10-0-0-206.ec2.internal, partition 3,PROCESS_LOCAL, 2033 bytes)
16/03/03 00:27:08 INFO TaskSetManager: Finished task 0.0 in stage 0.0 (TID 0) in 1460 ms on ip-10-0-0-206.ec2.internal (1/100)
16/03/03 00:27:08 INFO TaskSetManager: Starting task 4.0 in stage 0.0 (TID 4, ip-10-0-0-206.ec2.internal, partition 4,PROCESS_LOCAL, 2033 bytes)
16/03/03 00:27:08 INFO TaskSetManager: Finished task 3.0 in stage 0.0 (TID 3) in 116 ms on ip-10-0-0-206.ec2.internal (2/100)
16/03/03 00:27:08 INFO TaskSetManager: Starting task 5.0 in stage 0.0 (TID 5, ip-10-0-0-206.ec2.internal, partition 5,PROCESS_LOCAL, 2033 bytes)
16/03/03 00:27:08 INFO TaskSetManager: Finished task 4.0 in stage 0.0 (TID 4) in 101 ms on ip-10-0-0-206.ec2.internal (3/100)
16/03/03 00:27:08 INFO BlockManagerInfo: Added broadcast_0_piece0 in memory on ip-10-0-0-208.ec2.internal:58721 (size: 1186.0 B, free: 530.3 MB)
16/03/03 00:27:08 INFO TaskSetManager: Starting task 6.0 in stage 0.0 (TID 6, ip-10-0-0-206.ec2.internal, partition 6,PROCESS_LOCAL, 2033 bytes)
16/03/03 00:27:08 INFO TaskSetManager: Finished task 5.0 in stage 0.0 (TID 5) in 59 ms on ip-10-0-0-206.ec2.internal (4/100)
16/03/03 00:27:08 INFO TaskSetManager: Starting task 7.0 in stage 0.0 (TID 7, ip-10-0-0-206.ec2.internal, partition 7,PROCESS_LOCAL, 2033 bytes)
16/03/03 00:27:08 INFO TaskSetManager: Finished task 6.0 in stage 0.0 (TID 6) in 65 ms on ip-10-0-0-206.ec2.internal (5/100)
16/03/03 00:27:08 INFO TaskSetManager: Starting task 8.0 in stage 0.0 (TID 8, ip-10-0-0-206.ec2.internal, partition 8,PROCESS_LOCAL, 2033 bytes)
16/03/03 00:27:08 INFO TaskSetManager: Finished task 7.0 in stage 0.0 (TID 7) in 61 ms on ip-10-0-0-206.ec2.internal (6/100)
16/03/03 00:27:08 INFO TaskSetManager: Starting task 9.0 in stage 0.0 (TID 9, ip-10-0-0-206.ec2.internal, partition 9,PROCESS_LOCAL, 2033 bytes)
16/03/03 00:27:08 INFO TaskSetManager: Finished task 8.0 in stage 0.0 (TID 8) in 64 ms on ip-10-0-0-206.ec2.internal (7/100)
16/03/03 00:27:08 INFO TaskSetManager: Starting task 10.0 in stage 0.0 (TID 10, ip-10-0-0-206.ec2.internal, partition 10,PROCESS_LOCAL, 2036 bytes)
16/03/03 00:27:08 INFO TaskSetManager: Finished task 9.0 in stage 0.0 (TID 9) in 69 ms on ip-10-0-0-206.ec2.internal (8/100)
16/03/03 00:27:08 INFO TaskSetManager: Starting task 11.0 in stage 0.0 (TID 11, ip-10-0-0-208.ec2.internal, partition 11,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:08 INFO TaskSetManager: Starting task 12.0 in stage 0.0 (TID 12, ip-10-0-0-206.ec2.internal, partition 12,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:08 INFO TaskSetManager: Finished task 10.0 in stage 0.0 (TID 10) in 93 ms on ip-10-0-0-206.ec2.internal (9/100)
16/03/03 00:27:08 INFO TaskSetManager: Finished task 1.0 in stage 0.0 (TID 1) in 1366 ms on ip-10-0-0-208.ec2.internal (10/100)
16/03/03 00:27:08 INFO TaskSetManager: Starting task 13.0 in stage 0.0 (TID 13, ip-10-0-0-208.ec2.internal, partition 13,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:08 INFO TaskSetManager: Finished task 11.0 in stage 0.0 (TID 11) in 100 ms on ip-10-0-0-208.ec2.internal (11/100)
16/03/03 00:27:08 INFO TaskSetManager: Starting task 14.0 in stage 0.0 (TID 14, ip-10-0-0-206.ec2.internal, partition 14,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:08 INFO TaskSetManager: Finished task 12.0 in stage 0.0 (TID 12) in 101 ms on ip-10-0-0-206.ec2.internal (12/100)
16/03/03 00:27:08 INFO TaskSetManager: Starting task 15.0 in stage 0.0 (TID 15, ip-10-0-0-208.ec2.internal, partition 15,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 13.0 in stage 0.0 (TID 13) in 89 ms on ip-10-0-0-208.ec2.internal (13/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 16.0 in stage 0.0 (TID 16, ip-10-0-0-206.ec2.internal, partition 16,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 14.0 in stage 0.0 (TID 14) in 92 ms on ip-10-0-0-206.ec2.internal (14/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 17.0 in stage 0.0 (TID 17, ip-10-0-0-208.ec2.internal, partition 17,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 15.0 in stage 0.0 (TID 15) in 81 ms on ip-10-0-0-208.ec2.internal (15/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 18.0 in stage 0.0 (TID 18, ip-10-0-0-206.ec2.internal, partition 18,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 16.0 in stage 0.0 (TID 16) in 81 ms on ip-10-0-0-206.ec2.internal (16/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 19.0 in stage 0.0 (TID 19, ip-10-0-0-208.ec2.internal, partition 19,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO BlockManagerInfo: Added broadcast_0_piece0 in memory on ip-10-0-0-207.ec2.internal:60768 (size: 1186.0 B, free: 530.3 MB)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 17.0 in stage 0.0 (TID 17) in 80 ms on ip-10-0-0-208.ec2.internal (17/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 20.0 in stage 0.0 (TID 20, ip-10-0-0-206.ec2.internal, partition 20,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 18.0 in stage 0.0 (TID 18) in 78 ms on ip-10-0-0-206.ec2.internal (18/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 21.0 in stage 0.0 (TID 21, ip-10-0-0-208.ec2.internal, partition 21,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 19.0 in stage 0.0 (TID 19) in 64 ms on ip-10-0-0-208.ec2.internal (19/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 22.0 in stage 0.0 (TID 22, ip-10-0-0-206.ec2.internal, partition 22,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 20.0 in stage 0.0 (TID 20) in 80 ms on ip-10-0-0-206.ec2.internal (20/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 23.0 in stage 0.0 (TID 23, ip-10-0-0-208.ec2.internal, partition 23,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 21.0 in stage 0.0 (TID 21) in 87 ms on ip-10-0-0-208.ec2.internal (21/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 24.0 in stage 0.0 (TID 24, ip-10-0-0-206.ec2.internal, partition 24,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 22.0 in stage 0.0 (TID 22) in 70 ms on ip-10-0-0-206.ec2.internal (22/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 25.0 in stage 0.0 (TID 25, ip-10-0-0-208.ec2.internal, partition 25,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 23.0 in stage 0.0 (TID 23) in 71 ms on ip-10-0-0-208.ec2.internal (23/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 26.0 in stage 0.0 (TID 26, ip-10-0-0-206.ec2.internal, partition 26,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 24.0 in stage 0.0 (TID 24) in 67 ms on ip-10-0-0-206.ec2.internal (24/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 27.0 in stage 0.0 (TID 27, ip-10-0-0-208.ec2.internal, partition 27,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 25.0 in stage 0.0 (TID 25) in 55 ms on ip-10-0-0-208.ec2.internal (25/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 28.0 in stage 0.0 (TID 28, ip-10-0-0-206.ec2.internal, partition 28,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 26.0 in stage 0.0 (TID 26) in 48 ms on ip-10-0-0-206.ec2.internal (26/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 29.0 in stage 0.0 (TID 29, ip-10-0-0-208.ec2.internal, partition 29,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 28.0 in stage 0.0 (TID 28) in 57 ms on ip-10-0-0-206.ec2.internal (27/100)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 27.0 in stage 0.0 (TID 27) in 80 ms on ip-10-0-0-208.ec2.internal (28/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 30.0 in stage 0.0 (TID 30, ip-10-0-0-206.ec2.internal, partition 30,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 31.0 in stage 0.0 (TID 31, ip-10-0-0-207.ec2.internal, partition 31,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 32.0 in stage 0.0 (TID 32, ip-10-0-0-208.ec2.internal, partition 32,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 29.0 in stage 0.0 (TID 29) in 75 ms on ip-10-0-0-208.ec2.internal (29/100)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 2.0 in stage 0.0 (TID 2) in 1413 ms on ip-10-0-0-207.ec2.internal (30/100)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 30.0 in stage 0.0 (TID 30) in 49 ms on ip-10-0-0-206.ec2.internal (31/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 33.0 in stage 0.0 (TID 33, ip-10-0-0-206.ec2.internal, partition 33,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 34.0 in stage 0.0 (TID 34, ip-10-0-0-208.ec2.internal, partition 34,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 32.0 in stage 0.0 (TID 32) in 73 ms on ip-10-0-0-208.ec2.internal (32/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 35.0 in stage 0.0 (TID 35, ip-10-0-0-206.ec2.internal, partition 35,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 33.0 in stage 0.0 (TID 33) in 56 ms on ip-10-0-0-206.ec2.internal (33/100)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 31.0 in stage 0.0 (TID 31) in 98 ms on ip-10-0-0-207.ec2.internal (34/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 36.0 in stage 0.0 (TID 36, ip-10-0-0-207.ec2.internal, partition 36,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 37.0 in stage 0.0 (TID 37, ip-10-0-0-208.ec2.internal, partition 37,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 34.0 in stage 0.0 (TID 34) in 68 ms on ip-10-0-0-208.ec2.internal (35/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 38.0 in stage 0.0 (TID 38, ip-10-0-0-206.ec2.internal, partition 38,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 35.0 in stage 0.0 (TID 35) in 56 ms on ip-10-0-0-206.ec2.internal (36/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 39.0 in stage 0.0 (TID 39, ip-10-0-0-206.ec2.internal, partition 39,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 38.0 in stage 0.0 (TID 38) in 62 ms on ip-10-0-0-206.ec2.internal (37/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 40.0 in stage 0.0 (TID 40, ip-10-0-0-208.ec2.internal, partition 40,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 37.0 in stage 0.0 (TID 37) in 89 ms on ip-10-0-0-208.ec2.internal (38/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 41.0 in stage 0.0 (TID 41, ip-10-0-0-207.ec2.internal, partition 41,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 36.0 in stage 0.0 (TID 36) in 120 ms on ip-10-0-0-207.ec2.internal (39/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 42.0 in stage 0.0 (TID 42, ip-10-0-0-206.ec2.internal, partition 42,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 39.0 in stage 0.0 (TID 39) in 62 ms on ip-10-0-0-206.ec2.internal (40/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 43.0 in stage 0.0 (TID 43, ip-10-0-0-208.ec2.internal, partition 43,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 40.0 in stage 0.0 (TID 40) in 57 ms on ip-10-0-0-208.ec2.internal (41/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 44.0 in stage 0.0 (TID 44, ip-10-0-0-207.ec2.internal, partition 44,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 41.0 in stage 0.0 (TID 41) in 69 ms on ip-10-0-0-207.ec2.internal (42/100)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 42.0 in stage 0.0 (TID 42) in 52 ms on ip-10-0-0-206.ec2.internal (43/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 45.0 in stage 0.0 (TID 45, ip-10-0-0-206.ec2.internal, partition 45,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 43.0 in stage 0.0 (TID 43) in 58 ms on ip-10-0-0-208.ec2.internal (44/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 46.0 in stage 0.0 (TID 46, ip-10-0-0-208.ec2.internal, partition 46,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 44.0 in stage 0.0 (TID 44) in 61 ms on ip-10-0-0-207.ec2.internal (45/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 47.0 in stage 0.0 (TID 47, ip-10-0-0-207.ec2.internal, partition 47,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 45.0 in stage 0.0 (TID 45) in 58 ms on ip-10-0-0-206.ec2.internal (46/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 48.0 in stage 0.0 (TID 48, ip-10-0-0-206.ec2.internal, partition 48,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 46.0 in stage 0.0 (TID 46) in 63 ms on ip-10-0-0-208.ec2.internal (47/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 49.0 in stage 0.0 (TID 49, ip-10-0-0-208.ec2.internal, partition 49,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 47.0 in stage 0.0 (TID 47) in 56 ms on ip-10-0-0-207.ec2.internal (48/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 50.0 in stage 0.0 (TID 50, ip-10-0-0-207.ec2.internal, partition 50,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 51.0 in stage 0.0 (TID 51, ip-10-0-0-208.ec2.internal, partition 51,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 49.0 in stage 0.0 (TID 49) in 42 ms on ip-10-0-0-208.ec2.internal (49/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 52.0 in stage 0.0 (TID 52, ip-10-0-0-207.ec2.internal, partition 52,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 50.0 in stage 0.0 (TID 50) in 49 ms on ip-10-0-0-207.ec2.internal (50/100)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 51.0 in stage 0.0 (TID 51) in 38 ms on ip-10-0-0-208.ec2.internal (51/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 53.0 in stage 0.0 (TID 53, ip-10-0-0-208.ec2.internal, partition 53,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 54.0 in stage 0.0 (TID 54, ip-10-0-0-206.ec2.internal, partition 54,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 48.0 in stage 0.0 (TID 48) in 114 ms on ip-10-0-0-206.ec2.internal (52/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 55.0 in stage 0.0 (TID 55, ip-10-0-0-207.ec2.internal, partition 55,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 52.0 in stage 0.0 (TID 52) in 51 ms on ip-10-0-0-207.ec2.internal (53/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 56.0 in stage 0.0 (TID 56, ip-10-0-0-208.ec2.internal, partition 56,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 53.0 in stage 0.0 (TID 53) in 57 ms on ip-10-0-0-208.ec2.internal (54/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 57.0 in stage 0.0 (TID 57, ip-10-0-0-206.ec2.internal, partition 57,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 54.0 in stage 0.0 (TID 54) in 64 ms on ip-10-0-0-206.ec2.internal (55/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 58.0 in stage 0.0 (TID 58, ip-10-0-0-207.ec2.internal, partition 58,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 55.0 in stage 0.0 (TID 55) in 57 ms on ip-10-0-0-207.ec2.internal (56/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 59.0 in stage 0.0 (TID 59, ip-10-0-0-208.ec2.internal, partition 59,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 56.0 in stage 0.0 (TID 56) in 55 ms on ip-10-0-0-208.ec2.internal (57/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 60.0 in stage 0.0 (TID 60, ip-10-0-0-206.ec2.internal, partition 60,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:09 INFO TaskSetManager: Finished task 57.0 in stage 0.0 (TID 57) in 48 ms on ip-10-0-0-206.ec2.internal (58/100)
16/03/03 00:27:09 INFO TaskSetManager: Starting task 61.0 in stage 0.0 (TID 61, ip-10-0-0-207.ec2.internal, partition 61,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 58.0 in stage 0.0 (TID 58) in 69 ms on ip-10-0-0-207.ec2.internal (59/100)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 59.0 in stage 0.0 (TID 59) in 59 ms on ip-10-0-0-208.ec2.internal (60/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 62.0 in stage 0.0 (TID 62, ip-10-0-0-208.ec2.internal, partition 62,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 60.0 in stage 0.0 (TID 60) in 62 ms on ip-10-0-0-206.ec2.internal (61/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 63.0 in stage 0.0 (TID 63, ip-10-0-0-206.ec2.internal, partition 63,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 64.0 in stage 0.0 (TID 64, ip-10-0-0-207.ec2.internal, partition 64,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 61.0 in stage 0.0 (TID 61) in 74 ms on ip-10-0-0-207.ec2.internal (62/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 65.0 in stage 0.0 (TID 65, ip-10-0-0-208.ec2.internal, partition 65,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 62.0 in stage 0.0 (TID 62) in 66 ms on ip-10-0-0-208.ec2.internal (63/100)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 63.0 in stage 0.0 (TID 63) in 60 ms on ip-10-0-0-206.ec2.internal (64/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 66.0 in stage 0.0 (TID 66, ip-10-0-0-206.ec2.internal, partition 66,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 67.0 in stage 0.0 (TID 67, ip-10-0-0-207.ec2.internal, partition 67,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 64.0 in stage 0.0 (TID 64) in 71 ms on ip-10-0-0-207.ec2.internal (65/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 68.0 in stage 0.0 (TID 68, ip-10-0-0-208.ec2.internal, partition 68,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 65.0 in stage 0.0 (TID 65) in 63 ms on ip-10-0-0-208.ec2.internal (66/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 69.0 in stage 0.0 (TID 69, ip-10-0-0-206.ec2.internal, partition 69,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 66.0 in stage 0.0 (TID 66) in 47 ms on ip-10-0-0-206.ec2.internal (67/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 70.0 in stage 0.0 (TID 70, ip-10-0-0-207.ec2.internal, partition 70,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 67.0 in stage 0.0 (TID 67) in 55 ms on ip-10-0-0-207.ec2.internal (68/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 71.0 in stage 0.0 (TID 71, ip-10-0-0-208.ec2.internal, partition 71,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 68.0 in stage 0.0 (TID 68) in 50 ms on ip-10-0-0-208.ec2.internal (69/100)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 69.0 in stage 0.0 (TID 69) in 49 ms on ip-10-0-0-206.ec2.internal (70/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 72.0 in stage 0.0 (TID 72, ip-10-0-0-206.ec2.internal, partition 72,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 73.0 in stage 0.0 (TID 73, ip-10-0-0-207.ec2.internal, partition 73,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 70.0 in stage 0.0 (TID 70) in 63 ms on ip-10-0-0-207.ec2.internal (71/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 74.0 in stage 0.0 (TID 74, ip-10-0-0-208.ec2.internal, partition 74,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 75.0 in stage 0.0 (TID 75, ip-10-0-0-206.ec2.internal, partition 75,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 71.0 in stage 0.0 (TID 71) in 72 ms on ip-10-0-0-208.ec2.internal (72/100)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 72.0 in stage 0.0 (TID 72) in 56 ms on ip-10-0-0-206.ec2.internal (73/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 76.0 in stage 0.0 (TID 76, ip-10-0-0-207.ec2.internal, partition 76,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 73.0 in stage 0.0 (TID 73) in 58 ms on ip-10-0-0-207.ec2.internal (74/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 77.0 in stage 0.0 (TID 77, ip-10-0-0-208.ec2.internal, partition 77,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 74.0 in stage 0.0 (TID 74) in 67 ms on ip-10-0-0-208.ec2.internal (75/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 78.0 in stage 0.0 (TID 78, ip-10-0-0-206.ec2.internal, partition 78,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 75.0 in stage 0.0 (TID 75) in 75 ms on ip-10-0-0-206.ec2.internal (76/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 79.0 in stage 0.0 (TID 79, ip-10-0-0-207.ec2.internal, partition 79,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 76.0 in stage 0.0 (TID 76) in 56 ms on ip-10-0-0-207.ec2.internal (77/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 80.0 in stage 0.0 (TID 80, ip-10-0-0-208.ec2.internal, partition 80,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 77.0 in stage 0.0 (TID 77) in 62 ms on ip-10-0-0-208.ec2.internal (78/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 81.0 in stage 0.0 (TID 81, ip-10-0-0-206.ec2.internal, partition 81,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 82.0 in stage 0.0 (TID 82, ip-10-0-0-207.ec2.internal, partition 82,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 78.0 in stage 0.0 (TID 78) in 57 ms on ip-10-0-0-206.ec2.internal (79/100)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 79.0 in stage 0.0 (TID 79) in 44 ms on ip-10-0-0-207.ec2.internal (80/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 83.0 in stage 0.0 (TID 83, ip-10-0-0-206.ec2.internal, partition 83,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 81.0 in stage 0.0 (TID 81) in 36 ms on ip-10-0-0-206.ec2.internal (81/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 84.0 in stage 0.0 (TID 84, ip-10-0-0-207.ec2.internal, partition 84,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 82.0 in stage 0.0 (TID 82) in 46 ms on ip-10-0-0-207.ec2.internal (82/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 85.0 in stage 0.0 (TID 85, ip-10-0-0-206.ec2.internal, partition 85,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 83.0 in stage 0.0 (TID 83) in 35 ms on ip-10-0-0-206.ec2.internal (83/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 86.0 in stage 0.0 (TID 86, ip-10-0-0-207.ec2.internal, partition 86,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 84.0 in stage 0.0 (TID 84) in 46 ms on ip-10-0-0-207.ec2.internal (84/100)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 80.0 in stage 0.0 (TID 80) in 105 ms on ip-10-0-0-208.ec2.internal (85/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 87.0 in stage 0.0 (TID 87, ip-10-0-0-208.ec2.internal, partition 87,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 85.0 in stage 0.0 (TID 85) in 54 ms on ip-10-0-0-206.ec2.internal (86/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 88.0 in stage 0.0 (TID 88, ip-10-0-0-206.ec2.internal, partition 88,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 89.0 in stage 0.0 (TID 89, ip-10-0-0-207.ec2.internal, partition 89,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 86.0 in stage 0.0 (TID 86) in 65 ms on ip-10-0-0-207.ec2.internal (87/100)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 87.0 in stage 0.0 (TID 87) in 47 ms on ip-10-0-0-208.ec2.internal (88/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 90.0 in stage 0.0 (TID 90, ip-10-0-0-208.ec2.internal, partition 90,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 88.0 in stage 0.0 (TID 88) in 55 ms on ip-10-0-0-206.ec2.internal (89/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 91.0 in stage 0.0 (TID 91, ip-10-0-0-206.ec2.internal, partition 91,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 89.0 in stage 0.0 (TID 89) in 60 ms on ip-10-0-0-207.ec2.internal (90/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 92.0 in stage 0.0 (TID 92, ip-10-0-0-207.ec2.internal, partition 92,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 93.0 in stage 0.0 (TID 93, ip-10-0-0-208.ec2.internal, partition 93,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 90.0 in stage 0.0 (TID 90) in 59 ms on ip-10-0-0-208.ec2.internal (91/100)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 91.0 in stage 0.0 (TID 91) in 44 ms on ip-10-0-0-206.ec2.internal (92/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 94.0 in stage 0.0 (TID 94, ip-10-0-0-206.ec2.internal, partition 94,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 95.0 in stage 0.0 (TID 95, ip-10-0-0-207.ec2.internal, partition 95,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 92.0 in stage 0.0 (TID 92) in 56 ms on ip-10-0-0-207.ec2.internal (93/100)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 93.0 in stage 0.0 (TID 93) in 51 ms on ip-10-0-0-208.ec2.internal (94/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 96.0 in stage 0.0 (TID 96, ip-10-0-0-208.ec2.internal, partition 96,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 94.0 in stage 0.0 (TID 94) in 49 ms on ip-10-0-0-206.ec2.internal (95/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 97.0 in stage 0.0 (TID 97, ip-10-0-0-206.ec2.internal, partition 97,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 98.0 in stage 0.0 (TID 98, ip-10-0-0-207.ec2.internal, partition 98,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 95.0 in stage 0.0 (TID 95) in 66 ms on ip-10-0-0-207.ec2.internal (96/100)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 96.0 in stage 0.0 (TID 96) in 49 ms on ip-10-0-0-208.ec2.internal (97/100)
16/03/03 00:27:10 INFO TaskSetManager: Starting task 99.0 in stage 0.0 (TID 99, ip-10-0-0-208.ec2.internal, partition 99,PROCESS_LOCAL, 2037 bytes)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 97.0 in stage 0.0 (TID 97) in 49 ms on ip-10-0-0-206.ec2.internal (98/100)
16/03/03 00:27:10 INFO TaskSetManager: Finished task 98.0 in stage 0.0 (TID 98) in 48 ms on ip-10-0-0-207.ec2.internal (99/100)
16/03/03 00:27:10 INFO DAGScheduler: ResultStage 0 (reduce at SparkPi.scala:36) finished in 10.222 s
16/03/03 00:27:10 INFO DAGScheduler: Job 0 finished: reduce at SparkPi.scala:36, took 10.612260 s
16/03/03 00:27:10 INFO TaskSetManager: Finished task 99.0 in stage 0.0 (TID 99) in 38 ms on ip-10-0-0-208.ec2.internal (100/100)
16/03/03 00:27:10 INFO YarnScheduler: Removed TaskSet 0.0, whose tasks have all completed, from pool
16/03/03 00:27:10 INFO SparkUI: Stopped Spark web UI at http://10.0.0.60:4040
16/03/03 00:27:10 INFO DAGScheduler: Stopping DAGScheduler
16/03/03 00:27:10 INFO YarnClientSchedulerBackend: Interrupting monitor thread
16/03/03 00:27:10 INFO YarnClientSchedulerBackend: Shutting down all executors
16/03/03 00:27:10 INFO YarnClientSchedulerBackend: Asking each executor to shut down
16/03/03 00:27:10 INFO YarnClientSchedulerBackend: Stopped
16/03/03 00:27:10 INFO MapOutputTrackerMasterEndpoint: MapOutputTrackerMasterEndpoint stopped!
16/03/03 00:27:10 INFO MemoryStore: MemoryStore cleared
16/03/03 00:27:10 INFO BlockManager: BlockManager stopped
16/03/03 00:27:10 INFO BlockManagerMaster: BlockManagerMaster stopped
16/03/03 00:27:10 INFO OutputCommitCoordinator$OutputCommitCoordinatorEndpoint: OutputCommitCoordinator stopped!
16/03/03 00:27:10 INFO SparkContext: Successfully stopped SparkContext
16/03/03 00:27:10 INFO RemoteActorRefProvider$RemotingTerminator: Shutting down remote daemon.
16/03/03 00:27:10 INFO ShutdownHookManager: Shutdown hook called
16/03/03 00:27:10 INFO RemoteActorRefProvider$RemotingTerminator: Remote daemon shut down; proceeding with flushing remote transports.
16/03/03 00:27:10 INFO ShutdownHookManager: Deleting directory /tmp/spark-07df4e2a-afc8-4687-b30d-21a7b2d49a14

Running script on ephemeral scluster
16/03/03 00:27:15 INFO tools.DistCp: Input Options: DistCpOptions{atomicCommit=false, syncFolder=false, deleteMissing=false, ignoreFailures=false, maxMaps=20, sslConfigurationFile='null', copyStrategy='uniformsize', sourceFileListing=null, sourcePaths=[/user/ec2-user], targetPath=s3n://somekey:somesecret@bkvarda/ephemeral_output, targetPathExists=true, preserveRawXattrs=false, filtersFile='null'}
16/03/03 00:27:15 INFO client.RMProxy: Connecting to ResourceManager at ip-10-0-0-120.ec2.internal/10.0.0.120:8032
16/03/03 00:27:16 INFO tools.SimpleCopyListing: Paths (files+dirs) cnt = 5; dirCnt = 4
16/03/03 00:27:16 INFO tools.SimpleCopyListing: Build file listing completed.
16/03/03 00:27:16 INFO Configuration.deprecation: io.sort.mb is deprecated. Instead, use mapreduce.task.io.sort.mb
16/03/03 00:27:16 INFO Configuration.deprecation: io.sort.factor is deprecated. Instead, use mapreduce.task.io.sort.factor
16/03/03 00:27:16 INFO tools.DistCp: Number of paths in the copy list: 5
16/03/03 00:27:16 INFO tools.DistCp: Number of paths in the copy list: 5
16/03/03 00:27:16 INFO client.RMProxy: Connecting to ResourceManager at ip-10-0-0-120.ec2.internal/10.0.0.120:8032
16/03/03 00:27:17 INFO mapreduce.JobSubmitter: number of splits:1
16/03/03 00:27:17 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1456982691678_0002
16/03/03 00:27:17 INFO impl.YarnClientImpl: Submitted application application_1456982691678_0002
16/03/03 00:27:17 INFO mapreduce.Job: The url to track the job: http://ip-10-0-0-120.ec2.internal:8088/proxy/application_1456982691678_0002/
16/03/03 00:27:17 INFO tools.DistCp: DistCp job-id: job_1456982691678_0002
16/03/03 00:27:17 INFO mapreduce.Job: Running job: job_1456982691678_0002
16/03/03 00:27:24 INFO mapreduce.Job: Job job_1456982691678_0002 running in uber mode : false
16/03/03 00:27:24 INFO mapreduce.Job:  map 0% reduce 0%
16/03/03 00:27:36 INFO mapreduce.Job:  map 100% reduce 0%
16/03/03 00:27:38 INFO mapreduce.Job: Job job_1456982691678_0002 completed successfully
16/03/03 00:27:38 INFO mapreduce.Job: Counters: 38
	File System Counters
		FILE: Number of bytes read=0
		FILE: Number of bytes written=118327
		FILE: Number of read operations=0
		FILE: Number of large read operations=0
		FILE: Number of write operations=0
		HDFS: Number of bytes read=2186
		HDFS: Number of bytes written=0
		HDFS: Number of read operations=14
		HDFS: Number of large read operations=0
		HDFS: Number of write operations=2
		S3N: Number of bytes read=0
		S3N: Number of bytes written=1034
		S3N: Number of read operations=0
		S3N: Number of large read operations=0
		S3N: Number of write operations=0
	Job Counters
		Launched map tasks=1
		Other local map tasks=1
		Total time spent by all maps in occupied slots (ms)=9425
		Total time spent by all reduces in occupied slots (ms)=0
		Total time spent by all map tasks (ms)=9425
		Total vcore-seconds taken by all map tasks=9425
		Total megabyte-seconds taken by all map tasks=9651200
	Map-Reduce Framework
		Map input records=5
		Map output records=0
		Input split bytes=118
		Spilled Records=0
		Failed Shuffles=0
		Merged Map outputs=0
		GC time elapsed (ms)=71
		CPU time spent (ms)=2150
		Physical memory (bytes) snapshot=185729024
		Virtual memory (bytes) snapshot=1559580672
		Total committed heap usage (bytes)=210763776
	File Input Format Counters
		Bytes Read=1034
	File Output Format Counters
		Bytes Written=0
	org.apache.hadoop.tools.mapred.CopyMapper$Counter
		BYTESCOPIED=1034
		BYTESEXPECTED=1034
		COPY=5

Job complete, terminating the instance

```
