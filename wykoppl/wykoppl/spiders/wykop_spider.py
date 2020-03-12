import scrapy
import logging

from wykoppl.items import LinkItem, DownloadedItem
from scrapy.shell import inspect_response
from lxml import etree
from datetime import datetime
import dateutil.parser as dp

class WykopSpider(scrapy.Spider):
    name = "wykop"


    def start_requests(self):
        """return wykop sitemap link
        """
        urls = [
            'https://www.wykop.pl/sitemap.xml',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_main_xml)

    def parse_main_xml(self, response):
        """Extract links from wykop sitemap"""
        logging.debug("Processing first response")

        response.selector.remove_namespaces()
        links = response.xpath('//loc/text()').getall()

        # inspect_response(response)
        for link in links:
            if 'links' in link :
                logging.debug("Yielding url: %s" % link)
                yield scrapy.Request(url=link, callback=self.parse_link)

    def parse_link(self, response):
        """Extract links to znaleziska"""
        logging.debug("Processing first subsitemap: %s" % response.url)
        response.selector.remove_namespaces()
        selector = response.xpath('//url/loc/text()')

        for link in selector.getall():
            logging.debug("Downloading item: %s" % link)
            yield LinkItem(url=link)
            yield scrapy.Request(url=link, callback=self.parse_page)

    def parse_page(self, response):
        """Crate an item from the whole
        page content. Start downloading
        the comments."""
        logging.debug("Processing page: %s" % response.url)
        content = response.body

        datetime_string = response.xpath("//div[@class='space information bdivider']/div/p/b/*[@itemprop='datePublished']").attrib['datetime']
        dt= datetime.fromisoformat(datetime_string)

        yield DownloadedItem(
            url=response.url,
            title=response.url,
            tags='',
            page_code=content,
            publishing_date=dt,
            crawling_date=''
        )

        next_page = response.xpath('//a[class="button"][text()="następna"]').attrib['href']
        if next_page:
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

        response.xpath('//a[class="button"][text()="następna"]').attrib['href']

        datetime_string = response.xpath("//div[@class='space information bdivider']/div/p/b/*[@itemprop='datePublished']").attrib['datetime']
        dt= datetime.fromisoformat(datetime_string)

        yield DownloadedItem(
            url=response.url,
            title=meta['id'],
            tags='',
            page_code=content,
            publishing_date=dt,
            crawling_date=''
        )

        next_page = response.xpath('//a[class="button"][text()="następna"]').attrib['href']
        if next_page:
            yield scrapy.Request(url=next_page,
                                 callback=self.parse_page_comments,
                                 meta=meta)
