
# Getting started with docker

## Prerequisite: have docker up and working

To Install docker follow this link: (<https://docs.docker.com/get-docker/>)

Docker Cheatsheet: (<https://docs.docker.com/get-started/docker_cheatsheet.pdf>)

Please be aware, docker containers are stateless, if you want to store the state you need to use Volume Mapping(<https://github.com/wurstmeister/kafka-docker/issues/511>)

## Set Kafka Cluster up and ready

* Download lab files to your computer.

* Open up your command prompt

###  - Linux/Mac[*] 😍

Let's assume our *docker-compose.yml* file located in "/home/itoumlilt/Desktop/dauphine-streaming-labs" on Linux/Mac.

``` bash
cd "/home/itoumlilt/Desktop/dauphine-streaming-labs"
```

### - Windows[*]

Let's assume our *docker-compose.yml* file located in "C://Users/itoumlilt/Desktop/dauphine-streaming-labs" on our Windows.

``` bash
cd "C://Users/itoumlilt/Desktop/dauphine-streaming-labs"
```

### Get Git Repo

``` bash 
git clone https://github.com/wurstmeister/kafka-docker.git 
```

### Copy provided docker-compose.yml under kafka-dauphine-lab with wurstmeister's DockerFile

**Change directory inside of kafka-docker like you have done at stage[*]**

Once you are in kafka-docker folder run:

``` bash
docker-compose up
```

**Docker command compose-up could take around 30 secs**

**Check your logs, after kafka up you should see the following lines in your logs:**

```logs
ChangeEventProcessThread)
kafka_1      | [2022-02-22 20:26:37,324] INFO [SocketServer listenerType=ZK_BROKER, nodeId=1] Starting socket server acceptors and processors (kafka.network.SocketServer)
kafka_1      | [2022-02-22 20:26:37,363] INFO [SocketServer listenerType=ZK_BROKER, nodeId=1] Started data-plane acceptor and processor(s) for endpoint : ListenerName(PLAINTEXT) (kafka.network.SocketServer)
kafka_1      | [2022-02-22 20:26:37,366] INFO [SocketServer listenerType=ZK_BROKER, nodeId=1] Started socket server acceptors and processors (kafka.network.SocketServer)
kafka_1      | [2022-02-22 20:26:37,430] INFO Kafka version: 2.8.1 (org.apache.kafka.common.utils.AppInfoParser)
kafka_1      | [2022-02-22 20:26:37,431] INFO Kafka commitId: 839b886f9b732b15 (org.apache.kafka.common.utils.AppInfoParser)
kafka_1      | [2022-02-22 20:26:37,431] INFO Kafka startTimeMs: 1645561597367 (org.apache.kafka.common.utils.AppInfoParser)
kafka_1      | [2022-02-22 20:26:37,495] INFO [KafkaServer id=1] started (kafka.server.KafkaServer)
```

**please don't close your command line otherwise kafka will be killed**

Basically we made connection between your computers 9092 port with the container(kafkabroker's) 9092 so you can access it through your localhost.

So, Kafka broker will listen on **localhost:9092**, you can check docker-compose.yml for details.

**Open a new terminal, change directory like you have done at stage[*]**

**Download kafka-2.8.1 to kafka-dauphine-lab folder : <https://archive.apache.org/dist/kafka/2.8.0/kafka_2.12-2.8.0.tgz>**

**Unzip downloaded tgz folder and change directory(CD) inside of downloaded Kafka**

# Lab starts from here 👍

### 1) Create kafka topic

```bash
 bin/kafka-topics.sh --create --topic dauphine-test-topic --bootstrap-server localhost:9092
```

#### 2) Observe your change

The following command should print all created topics:

```bash
 bin/kafka-topics.sh --describe --bootstrap-server localhost:9092
```

But you can list per topic as well by adding --topic dauphine-test-topic

You can change topic details with --alter
```bash
 bin/kafka-topics.sh --alter --topic dauphine-test-topic --bootstrap-server localhost:9092
```

**1st question:** how could we change retention of topic ? Is retention just time-based ?

### 3) Produce (Write) your data into Kafka

```bash
 bin/kafka-console-producer.sh --topic dauphine-test-topic --bootstrap-server localhost:9092
```

 To stop producing data, you can press Ctrl-C at any time.

**2nd question:** what is idempotency ? How could we enable idempotency on Kafka producers ?

**3rd question:** how could we change ack? What is difference between acks=0/acks=1/acks=all ?

### 4) Consumer(Read) your data from Kafka

```bash
 bin/kafka-console-consumer.sh --topic dauphine-test-topic --from-beginning --bootstrap-server localhost:9092
```

You can also use consumer group (in such scenario your partitions will be shared across multiple consumers)

```bash
 bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --topic dauphine-test-topic --consumer-property group.id=my-consumer-first-group
```

Please remember group-id tracked by kafka cluster, so you can see the progress on broker-side:

```bash
bin/kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group foo
```

Here you could also **observe**:
**4th question:** what happens topic with one partition consumed with multiple consumers(all consumers have same consumer group id)
**5th question:** what happens topic with ten partitions, consumed by two consumers(all consumers have same  same consumer group id)

### 5) Custom Producer-Consumer

**Note: you can use localhost:9092 as kafka endpoint**

5.1. Use your favourite programming languages (or either provided python script) and produce random gps coordinates with order into topic called gps_locations

Latitude(Lat): [-90.00000, 90.00000], Longitude(Long): [-180.00000,180.00000]

For instance(Header:Order Lat,Long)

```
1 33.45384,135.34856
2 -39.61062,68.95387
3 -19.61062,48.32187
4 29.61062,28.94387
```

5.2. Use your favourite programming languages and consume(print) stored data (from topic called dauphine-test-topic) on Kafka broker.

5.3. How does enable.auto.commit variable changes consumer behaviour:(**6th question**)

    * set enable.auto.commit to false on consumer: it is enabled by default, make sure you generated few thousands records. Start your consumer for a second then stop it(ctrl+c), once you start again you should

### Optional: 6)kcat (formerly kafkacat)

To Install: <https://github.com/edenhill/kcat>

#### kcat: Metadata List Mode

In metadata list mode (-L), kafkacat displays metadata which includes Kafka topics, partitions, replicas and in-sync replicas (ISR).

``` bash
kcat -b localhost:9092 -L
```

if you are looking for JSON use, -J make it more prettier(you need ot have jq)

```bash
kcat -b localhost:9092 -L -J | jq .
```

#### kcat: Producer Mode

In producer mode, kafkacat reads messages from standard input (stdin).

-b broker -t topic -D delimeter(default is new line)

``` bash
kcat -b localhost:9092 -t "topic_name_should_be_here" -P
```

You can direct any file fully to kcat it will be published. Let’s assume we want to writesyslog(/var/log/syslog) file to kafka, so you can use the following command (- Linux/MAC only):

``` bash
cat /var/log/syslog | kcat -b localhost:9092 -t "topic_name_should_be_here" -z snappy
```

#### Kcat: Consumer Mode

``` bash
kcat -C -b localhost:9092 -t "topic_name_should_be_here"
```

* -e exist when finished

``` bash
kcat -C -b localhost:9092 -t "topic_name_should_be_here" -e`
```

* -o offset(starting from)

``` bash
kcat  -C -b localhost:9092 -t "topic_name_should_be_here" -o 5`
```

* -G group

``` bash
kcat -b localhost:9092 -G groupNumber1 "topic_name_should_be_here" "topic2_name_should_be_here"
```

* -p partition: -p 5 tells kafkacat to only read messages from partition 5.

``` bash
kcat -C -b localhost:9092 -t "topic_name_should_be_here" -p 5 -e
```