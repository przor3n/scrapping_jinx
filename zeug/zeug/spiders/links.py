import scrapy
import logging

from zeug.items import LinkItem, DownloadedItem
from zeug.db import Scraps, Links, Downloads
from scrapy.shell import inspect_response
from lxml import etree
from zeug.pages.wykop import Wykop
from zeug.db import retrive_downloads
from zeug.spiders.webpage_spider import WebpageSpider, PO, Item

class LinksSpider(WebpageSpider):
    name = "links"

    def start_requests(self):
        """return wykop sitemap link
        """

        callback = self.parse_list

        if PO.is_single:
            callback = self.parse_single


        for link in retrive_downloads():
            try:
                yield scrapy.Request(url=url, callback=callback)
            except ValueError:
                pass
