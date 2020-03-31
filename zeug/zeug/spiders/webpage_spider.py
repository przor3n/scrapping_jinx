import scrapy
import logging
import time

from zeug.items import LinkItem, DownloadedItem
from scrapy.shell import inspect_response
from lxml import etree
from datetime import datetime
from zeug.pages import get_page_object
from zeug.pages.wykop import Wykop

from zeug.env import SPIDER_OUTPUT_ITEM, PAGE_MODULE, PAGE_OBJECT

Items = {'DownloadedItem': DownloadedItem, 'LinkItem': LinkItem}
Item = Items.get(SPIDER_OUTPUT_ITEM)

PO = get_page_object(PAGE_MODULE, PAGE_OBJECT)


class WebpageSpider(scrapy.Spider):
    name = "webpage_spider"

    def start_requests(self):
        """Start request by downloading urls. """

        callback = self.parse_list

        if PO.is_single:
            callback = self.parse_single

        for url in PO.start_urls:
            yield scrapy.Request(url=url, callback=callback)

    def parse_single(self, response):
        """Handle single page"""
        self.logger.info("Downloaded page %s", response.url)

        PO.is_xml and response.selector.remove_namespaces()

        yield Item.load_item(response, PO)
        yield from self.extract_content_pagination_links(response)

    def parse_list(self, response):
        """Handle list page"""
        self.logger.info("Downloaded page %s", response.url)

        PO.is_xml and response.selector.remove_namespaces()

        yield from self.extract_content_links(response)
        yield from self.extract_list_links(response)
        yield from self.extract_list_pagination_links(response)

    def extract_content_links(self, response):
        """Extract content links and parse it"""
        for url in PO.content_links(response):
            yield scrapy.Request(url=url, callback=self.parse_single)

    def extract_list_links(self, response):
        """Extract list links and parse it"""
        for url in PO.list_links(response):
            yield scrapy.Request(url=url, callback=self.parse_list)

    def extract_content_pagination_links(self, response):
        """Extract content pagination links and parse it"""
        meta = {'parent': response.url}
        for url in PO.content_pagination_links(response):

            yield scrapy.Request(url=url,
                                 callback=self.parse_single,
                                 meta=meta)

    def extract_list_pagination_links(self, response):
        """Extract list pagination links and parse it"""
        for url in PO.list_pagination_links(response):
            yield scrapy.Request(url=url, callback=self.parse_list)