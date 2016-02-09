###Performance 

####How do I benchmark a cluster?

#####Teragen/Terasort/Teravalidate
Teragen writes X sized file to HDFS in 100 byte increments consisting of a randomly generated key and a random value. Terasort reads the data written by teragen and sorts it, with it's output also written to HDFS. Teravalidate reads the output from terasort to validate that it was indeed sorted.  
######What does it measure?
Teragen is effectively an HDFS write performance test. Terasort is an HDFS I/O/throughput, network throughput, CPU, and memory test (it effectively exercises everything). Teravalidate is effectively a HDFS read performance test. 
######How do I run it?
First, Teragen is ran like so:
```
hadoop jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar teragen 4000000 /user/ec2-user/test1
```
The above will create write 400MB to the directory /user/ec2-user/test1 on HDFS. It will do so using the default number of mappers. Note that 4000000 specified = 400MB. That is because 400000 is the number of 100 byte lines being written. 

The output of the above command looks like this:
```
16/02/08 20:12:39 INFO client.RMProxy: Connecting to ResourceManager at ip-10-0-0-197.ec2.internal/10.0.0.197:8032
16/02/08 20:12:39 INFO terasort.TeraSort: Generating 4000000 using 2
16/02/08 20:12:39 INFO mapreduce.JobSubmitter: number of splits:2
16/02/08 20:12:39 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1454969046055_0001
16/02/08 20:12:40 INFO impl.YarnClientImpl: Submitted application application_1454969046055_0001
16/02/08 20:12:40 INFO mapreduce.Job: The url to track the job: http://ip-10-0-0-197.ec2.internal:8088/proxy/application_1454969046055_0001/
16/02/08 20:12:40 INFO mapreduce.Job: Running job: job_1454969046055_0001
16/02/08 20:12:47 INFO mapreduce.Job: Job job_1454969046055_0001 running in uber mode : false
16/02/08 20:12:47 INFO mapreduce.Job:  map 0% reduce 0%
16/02/08 20:12:56 INFO mapreduce.Job:  map 50% reduce 0%
16/02/08 20:12:57 INFO mapreduce.Job:  map 100% reduce 0%
16/02/08 20:12:57 INFO mapreduce.Job: Job job_1454969046055_0001 completed successfully
16/02/08 20:12:57 INFO mapreduce.Job: Counters: 31
	File System Counters
		FILE: Number of bytes read=0
		FILE: Number of bytes written=231290
		FILE: Number of read operations=0
		FILE: Number of large read operations=0
		FILE: Number of write operations=0
		HDFS: Number of bytes read=167
		HDFS: Number of bytes written=400000000
		HDFS: Number of read operations=8
		HDFS: Number of large read operations=0
		HDFS: Number of write operations=4
	Job Counters 
		Launched map tasks=2
		Other local map tasks=2
		Total time spent by all maps in occupied slots (ms)=14571
		Total time spent by all reduces in occupied slots (ms)=0
		Total time spent by all map tasks (ms)=14571
		Total vcore-seconds taken by all map tasks=14571
		Total megabyte-seconds taken by all map tasks=14920704
	Map-Reduce Framework
		Map input records=4000000
		Map output records=4000000
		Input split bytes=167
		Spilled Records=0
		Failed Shuffles=0
		Merged Map outputs=0
		GC time elapsed (ms)=138
		CPU time spent (ms)=10210
		Physical memory (bytes) snapshot=710615040
		Virtual memory (bytes) snapshot=3138387968
		Total committed heap usage (bytes)=840957952
	org.apache.hadoop.examples.terasort.TeraGen$Counters
		CHECKSUM=8589195671261976
	File Input Format Counters 
		Bytes Read=0
	File Output Format Counters 
		Bytes Written=400000000
```
Notice that the number of mappers is 2. That isn't really going to push our cluster. What we need to do is use as many resources as we can to push the cluster as much as possible. To do this, we'll pass a flag to teragen that will specify more mappers. To start, you might set the number of mappers to (number of total cores on data nodes - 1). In my scenario, I have 3 datanodes each with 2 cores, so I will use 5 mappers. Note that this number might need to be increased to use more CPU/memory resources and really push the nodes. 

```
hadoop jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar teragen -Dmapred.map.tasks=5 4000000 /user/ec2-user/test2
```
You should time the amount of time the task takes, just prepend with time:
```
time hadoop jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar teragen -Dmapred.map.tasks=5 4000000 /user/ec2-user/test2
```
Your time results will look like this:
```
real	0m18.930s
user	0m5.753s
sys	0m0.231s
```
You can roughly measure your write bandwidth by dividing the # of bytes written by the duration of the task

Once teragen is complete, you want to terasort. You'll want to terasort and specify the number of reduce tasks - number of data node cores / 2 is a good starting point for reducers.
```
time hadoop jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar terasort -Dmapred.reduce.tasks=3 /user/ec2-user/test2 /user/ec2-user/terasort2

```
For terasort/teragen, you'll want to make sure that the cluster CPU and/or memory is fully maxed. You may need to adjust the number of reducers, mappers, or the amount of memory to each (Dmapreduce.map.memory.mb=2048 and Dmapreduce.reduce.memory.mb=2048 flags respectively where 2048 is the memory per reducer/mapper) in order to max out CPU and/or ram. 

For teravalidate, you don't really have to specify mapper or reducer quantities because it will pick the appropriate # of mappers for you (equal to the # of files from the terasort) and the reduce doesn't really matter (simply returns a small amount of output).

```
time hadoop jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar teravalidate /user/ec2-user/terasort2 /user/ec2-user/teravalidate
```
If you have cloudera manager, looking at the HDFS IO, Cluster CPU, Disk IO, and Cluster Network IO charts on the cluster home page is pretty good for seeing what's going on. You might also look at the charts under YARN as well.

#####TestDFSIO
Tests read/write I/O/bandwidth capabilities of your cluster.
######How does it work?
Writes N number of files of X size to /benchmarks/TestDFSIO on HDFS, and subsequently can read them. For each file being written, one mapper is used. 
######Write test
First, make sure the /benchmarks in directory is read/writeable by the user executing TestDFSIO:
```
sudo -u hdfs hdfs dfs -mkdir /benchmarks
sudo -u hdfs hdfs dfs -chown ec2-user:ec2-user /benchmarks
```
Then execute the write test:
```
hadoop jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-mapreduce-client-jobclient.jar TestDFSIO -write -nrFiles 16 -fileSize 1GB
```
The above writes 16 files of size 1GB, with 16 mappers. If possible, increase mappers until either A) your CPU maxes out or B) your HDFS IO/Disk IO peaks. At the end of the test, you'll get results like this:
```
16/02/08 23:19:21 INFO fs.TestDFSIO: ----- TestDFSIO ----- : write
16/02/08 23:19:21 INFO fs.TestDFSIO:            Date & time: Mon Feb 08 23:19:21 EST 2016
16/02/08 23:19:21 INFO fs.TestDFSIO:        Number of files: 16
16/02/08 23:19:21 INFO fs.TestDFSIO: Total MBytes processed: 16384.0
16/02/08 23:19:21 INFO fs.TestDFSIO:      Throughput mb/sec: 11.296715995567915
16/02/08 23:19:21 INFO fs.TestDFSIO: Average IO rate mb/sec: 12.506854057312012
16/02/08 23:19:21 INFO fs.TestDFSIO:  IO rate std deviation: 4.397178427944903
16/02/08 23:19:21 INFO fs.TestDFSIO:     Test exec time sec: 186.668
16/02/08 23:19:21 INFO fs.TestDFSIO: 
```
To execute the read test:
```
hadoop jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-mapreduce-client-jobclient.jar TestDFSIO -read -nrFiles 16 -fileSize 1GB
```
At the end of the test, you will get results like this:
```
16/02/08 23:22:27 INFO fs.TestDFSIO: ----- TestDFSIO ----- : read
16/02/08 23:22:27 INFO fs.TestDFSIO:            Date & time: Mon Feb 08 23:22:27 EST 2016
16/02/08 23:22:27 INFO fs.TestDFSIO:        Number of files: 16
16/02/08 23:22:27 INFO fs.TestDFSIO: Total MBytes processed: 16384.0
16/02/08 23:22:27 INFO fs.TestDFSIO:      Throughput mb/sec: 168.42451530664692
16/02/08 23:22:27 INFO fs.TestDFSIO: Average IO rate mb/sec: 311.3224792480469
16/02/08 23:22:27 INFO fs.TestDFSIO:  IO rate std deviation: 240.68966957443234
16/02/08 23:22:27 INFO fs.TestDFSIO:     Test exec time sec: 36.52
16/02/08 23:22:27 INFO fs.TestDFSIO:
```
One thing you'll notice about my results is that my read MB/sec is much higher than my write MB/sec (this test took place in AWS)

