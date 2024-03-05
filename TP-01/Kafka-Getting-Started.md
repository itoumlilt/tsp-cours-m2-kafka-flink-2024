# Kafka Getting Started

## Prerequisites

This tutorial assumes you are starting fresh and have no existing Kafka or ZooKeeper data. Since Kafka console scripts are different for Unix-based and Windows platforms, on Windows platforms use `bin\windows\` instead of `bin/`, and change the script extension to `.bat`.

## Download Kafka

```bash
wget https://dlcdn.apache.org/kafka/3.4.0/kafka_2.13-3.4.0.tgz

tar xzvf kafka_2.13-3.4.0.tgz
``` 

## Start Zookeeper

```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```

Check that Zookeeper is correctly running

```
$ telnet localhost 5181
Trying ::1...
Connected to localhost.
Escape character is '^]'.
srvr
Zookeeper version: 3.6.3--6401e4ad2087061bc6b9f80dec2d69f2e3c8660a, built on 04/08/2021 16:35 GMT
Latency min/avg/max: 0/0.0/0
Received: 1
Sent: 0
Connections: 1
Outstanding: 0
Zxid: 0x0
Mode: standalone
Node count: 5
Connection closed by foreign host.
```

## Start Kafka

```
bin/kafka-server-start.sh config/server.properties
```

## Create a Topic

```
$ bin/kafka-topics.sh --create --topic iasd-getting-started --bootstrap-server localhost:9092
Created topic iasd-getting-started.
```

Tip: run `bin/kafka-topics.sh` command without arguments to print usage information

For example, to describe our topic:

```
$ bin/kafka-topics.sh --describe --topic iasd-getting-started --bootstrap-server localhost:9092
Topic: iasd-getting-started	TopicId: o3wFw7QNRaCJwE2r82Ns7A	PartitionCount: 1	ReplicationFactor: 1	Configs:
    Topic: iasd-getting-started	Partition: 0	Leader: 0	Replicas: 0	Isr: 0
```

## Write some events into the topic:

Run the console producer client to write a few events into your topic. 

By default, each line you enter will result in a separate event being written to the topic

```
bin/kafka-console-producer.sh --topic iasd-getting-started --bootstrap-server localhost:9092
>Hello IASD!
>Here is another event
>^C
```

## Read the events:

To read the events you just created:

```
bin/kafka-console-consumer.sh --topic iasd-getting-started --from-beginning --bootstrap-server localhost:9092
Hello IASD!
Here is another event
^CProcessed a total of 2 messages
```

## Try out:

Open producer in one terminal and consumer in another and observe events immediately showing up in the consumer side