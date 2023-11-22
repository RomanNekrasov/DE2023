import logging
import time
from threading import Thread

from kafka import KafkaConsumer, TopicPartition


def read_from_topic(kafka_consumer, topic):
    kafka_consumer.subscribe(topics=[topic])
    for msg in kafka_consumer:
        print(msg.value.decode("utf-8"))


def read_from_topic_with_partition(kafka_consumer, topic):
    kafka_consumer.assign([TopicPartition(topic, 1)])
    for msg in kafka_consumer:
        print(msg)


def read_from_topic_with_partition_offset(kafka_consumer, topic):
    partition = TopicPartition(topic, 0)
    kafka_consumer.assign([partition])
    last_offset = kafka_consumer.end_offsets([partition])[partition]
    for msg in kafka_consumer:
        if msg.offset == last_offset - 1:
            break


# if you want to learn about threading in python, check the following article
# https://realpython.com/intro-to-python-threading/

class KafkaMessageConsumer(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.consumer = KafkaConsumer(bootstrap_servers='34.27.74.158:9092',  # use your VM's external IP Here!
                                      auto_offset_reset='earliest',
                                      consumer_timeout_ms=10000)
        self.start()

    def run(self):
        while True:
            try:
                read_from_topic(self.consumer, 'wordcount')
                time.sleep(30)
            except Exception as err:
                logging.info(f"Unexpected {err=}, {type(err)=}")
                time.sleep(30)
