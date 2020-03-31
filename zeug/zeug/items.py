# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from datetime import datetime
from scrapy.loader import ItemLoader


class LinkItem(scrapy.Item):
    url = scrapy.Field()

    @staticmethod
    def load_item(response, page_object):
        l = ItemLoader(item=LinkItem(), response=response)
        l.add_value('url', response.url)
        return l.load_item()


class DownloadedItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    tags = scrapy.Field()
    page_code = scrapy.Field()
    publishing_date = scrapy.Field()
    crawling_date = scrapy.Field()

    @staticmethod
    def load_item(response, page_object):
        l = ItemLoader(item=DownloadedItem(), response=response)
        l.add_value('tags', page_object.tags(response))
        l.add_value('title', page_object.title(response))
        l.add_value('page_code', response._get_body().encode('utf-8'))
        l.add_value('url', response.url)
        l.add_value('publishing_date', page_object.publish_date(response))
        l.add_value('crawling_date', datetime.now())

        if 'parent' in response.meta:
            l.add_value('parent', response.meta['parent'])
        else:
            l.add_value('parent', '')

        return l.load_item()