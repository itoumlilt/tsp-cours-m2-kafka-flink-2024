# you may need to install pip install kafka-python
from kafka import KafkaProducer
import random

# assume kafka broker on localhost:9092
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))


for e in range(1000):
    data = {'number' : e}
    producer.send('topic-name-should-be-here', value=data)
    sleep(random.uniform(0, 2))

