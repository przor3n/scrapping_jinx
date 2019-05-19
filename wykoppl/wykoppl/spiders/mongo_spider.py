import scrapy
import logging
import pymongo
from scrapy.shell import inspect_response
from lxml import etree

client = pymongo.MongoClient('mongo.lucifer', 27017)
mn_links = client.db.wykop_links
mn_pages = client.db.wykop_pages

class MongoSpider(scrapy.Spider):
    name = "wykopmongo"

    def start_requests(self):
        """return wykop sitemap link
        """

        for obj in mn_links.find():
            url = obj.get('url', None)
            if url is None:
                continue
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        """Crate an item from the whole
        page content. Start downloading
        the comments."""
        logging.debug("Processing page: %s" % response.url)
        content = response.body

        page = {
            'id': response.url,
            'url': response.url,
            'content': content
        }
        mn_pages.insert_one(page)

        next_page = response.xpath('//a[@class="button"][text()="następna"]')

        if next_page:
            url = next_page.attrib['href']
            meta = {'id': response.url}
            yield scrapy.Request(url=url,
                                 callback=self.parse_page_comments,
                                 meta=meta)

    def parse_page_comments(self, response):
        """Create and item from the comments
        page. then yield next page, use this
        function callback."""
        logging.debug("Processing comment page: %s" % response.url)
        meta = response.meta
        content = response.body

        page = {
            'id': meta['id'],
            'url': response.url,
            'content': content
        }
        mn_pages.insert_one(page)

        next_page = response.xpath('//a[@class="button"][text()="następna"]')
        if next_page:
            url = next_page.attrib['href']
            yield scrapy.Request(url=url,
                                 callback=self.parse_page_comments,
                                 meta=meta)
