import scrapy
import logging

from wykoppl.items import LinkItem, DownloadedItem
from wykoppl.items import Scraps, Links, Downloads
from scrapy.shell import inspect_response
from lxml import etree
from wykoppl.pages.wykop import Wykop
from wykoppl.db import session


from kafka import KafkaConsumer

class LinksSpider(scrapy.Spider):
    name = "links"

    def start_requests(self):
        """return wykop sitemap link
        """

        for link in session.query(Downloads). \
                filter(Downloads.downloaded == 0).limit(50000). \
                all():

            url = link.url.replace("http://", "https://")

            try:
                yield scrapy.Request(url=url, callback=self.parse_page)
            except ValueError:
                pass

    def parse_page(self, response):
        """Crate an item from the whole
        page content. Start downloading
        the comments."""
        logging.debug("Processing page: %s" % response.url)
        content = response.body

        yield DownloadedItem(
            url=response.url,
            title=response.url,
            tags='',
            page_code=content,
            publishing_date=Wykop.publish_date(response),
            crawling_date=''
        )

        for next_page in Wykop.next_pages(response):
            meta = {'id': response.url}
            yield scrapy.Request(url=next_page,
                                 callback=self.parse_page_comments,
                                 meta=meta)

    def parse_page_comments(self, response):
        """Create and item from the comments
        page. then yield next page, use this
        function callback."""
        logging.debug("Processing comment page: %s" % response.url)
        meta = response.meta
        content = response.body

        yield DownloadedItem(
            url=response.url,
            title=meta['id'],
            tags='',
            page_code=content,
            publishing_date=Wykop.publish_date(response),
            crawling_date=''
        )

        for next_page in Wykop.next_pages(response):
            yield scrapy.Request(url=next_page,
                                 callback=self.parse_page_comments,
                                 meta=meta)


class KafkaLinksSpider(scrapy.Spider):
    name = "kafka_links"

    def start_requests(self):
        """return wykop sitemap link
        """

        for link in session.query(Downloads). \
                filter(Downloads.downloaded == 0).limit(50000). \
                all():

            url = link.url.replace("http://", "https://")

            try:
                yield scrapy.Request(url=url, callback=self.parse_page)
            except ValueError:
                pass