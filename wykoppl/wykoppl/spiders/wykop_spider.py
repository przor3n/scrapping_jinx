import scrapy
import logging

from wykoppl.items import LinkItem, DownloadedItem
from scrapy.shell import inspect_response
from lxml import etree
from datetime import datetime
from wykoppl.pages.wykop import Wykop

class WykopSpider(scrapy.Spider):
    name = "wykop"


    def start_requests(self):
        """return wykop sitemap link
        """
        urls = [
            Wykop.sitemap_url,
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_main_xml)

    def parse_main_xml(self, response):
        """Extract links from wykop sitemap"""
        logging.debug("Processing first response")

        response.selector.remove_namespaces()
        links = response.xpath(Wykop.first_tier_sitemaps_xpath).getall()

        # inspect_response(response)
        for link in links:
            if 'links' in link :
                logging.debug("Yielding url: %s" % link)
                yield scrapy.Request(url=link, callback=self.parse_link)

    def parse_link(self, response):
        """Extract links to znaleziska"""
        logging.debug("Processing first subsitemap: %s" % response.url)
        response.selector.remove_namespaces()
        selector = response.xpath(Wykop.second_tier_links_xpath)

        for link in selector.getall():
            logging.debug("Downloading item: %s" % link)
            yield LinkItem(url=link)
