# -*- coding: utf-8 -*-
import scrapy


class LinksCrawlerSpider(scrapy.Spider):
    name = 'links_crawler'
    allowed_domains = ['general_service']
    start_urls = ['http://general_service/']

    def parse(self, response):
        pass

    def parse_page(self, response):
        """Crate an item from the whole
        page content. Start downloading
        the comments."""
        logging.debug("Processing page: %s" % response.url)
        content = response.body

        yield DownloadedItem()


        
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