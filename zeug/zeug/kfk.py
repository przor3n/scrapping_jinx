#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zeug.env import (
    CONSUMER_TOPIC,
    CONSUMER_GROUP,
    KAFKA_CONSUMER_SERVER,
)

from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka.errors import KafkaError

link_consumer = KafkaConsumer(CONSUMER_TOPIC,
                              group_id=CONSUMER_GROUP,
                              bootstrap_servers=[KAFKA_CONSUMER_SERVER])

assert link_consumer, 'Link Consumer not present'