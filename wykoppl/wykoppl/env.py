from os import environ

DB_CONNECTION = environ.get('DB_CONNECTION')
DB_SCHEMA = environ.get('DB_SCHEMA')

LINK_CONSUMER_TOPIC = environ.get('LINK_CONSUMER_TOPIC')
LINK_CONSUMER_GROUP = environ.get('LINK_CONSUMER_GROUP')
KAFKA_CONSUMER_SERVER = environ.get('KAFKA_CONSUMER_SERVER')

SPIDER_OUTPUT_ITEM = environ.get('SPIDER_OUTPUT_ITEM', 'DownloadedItem')

PAGE_MODULE = environ.get('PAGE_MODULE')
PAGE_OBJECT = environ.get('PAGE_OBJECT')

assert PAGE_MODULE, "PAGE_MODULE is required for crawler"
assert PAGE_OBJECT, "PAGE_OBJECT is required for crawler"