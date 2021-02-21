import scrapy
import logging
import time
import glob

from zeug.items import LinkItem, DownloadedItem
from scrapy.shell import inspect_response
from lxml import etree
from datetime import datetime
from zeug.pages import get_page_object
from zeug.pages.wykop import Wykop

from zeug.env import (
    SPIDER_OUTPUT_ITEM, PAGE_MODULE, PAGE_OBJECT, GLOB_PATTERN)

Items = {'DownloadedItem': DownloadedItem, 'LinkItem': LinkItem}
Item = Items.get(SPIDER_OUTPUT_ITEM)

PO = None # get_page_object(PAGE_MODULE, PAGE_OBJECT)


class FilesystemSpider(scrapy.Spider):
    name = "kafka_spider"

    def start_requests(self):
        """Start request by downloading urls. """

        for message in glob.iglob(GLOB_PATTERN, recursive=True):
            # message value and key are raw bytes -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            #print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
            #                                    message.offset, message.key,
            #                                    message.value))

            key, value = message.key.decode('utf-8'), message.value.decode(
                'utf-8')

            yield scrapy.Request(url=key,
                                 callback=self.parse_single,
                                 meta=json.loads(value))

    def parse_single(self, response):
        """Handle single page"""
        self.logger.info("Downloaded page %s", response.url)
        yield Item.load_item(response, PO)
