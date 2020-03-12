#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wykoppl.env import (DB_CONNECTION,
                         LINK_CONSUMER_TOPIC,
                         LINK_CONSUMER_GROUP,
                         KAFKA_CONSUMER_SERVER,
                         )

from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka.errors import KafkaError

# this has to be only one
# engine = create_engine('sqlite:///file.db')
engine = create_engine(DB_CONNECTION)

assert engine, 'Engine not set'

Session = sessionmaker(bind=engine)
session = Session() # use session object

assert session, 'Session not set'


link_consumer = KafkaConsumer(LINK_CONSUMER_TOPIC,
                         group_id=LINK_CONSUMER_GROUP,
                         bootstrap_servers=[KAFKA_CONSUMER_SERVER])


assert link_consumer, 'Link Consumer not present'