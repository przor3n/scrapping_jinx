# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from datetime import datetime
from scrapy.loader import ItemLoader

from sqlalchemy.ext.declarative import declarative_base
from wykoppl.db import engine
from sqlalchemy import (
    MetaData,
    Column,
    Integer,
    Text,
    String,
    DateTime,
    LargeBinary,
)

from wykoppl.env import DB_SCHEMA

meta = MetaData(schema=DB_SCHEMA)

Base = declarative_base(metadata=meta)


class WebentityMixin:
    id = Column(Integer, primary_key=True)
    url = Column(String(400))

    @classmethod
    def make(cls, item):
        return cls(url=item['url'])


class PageMixin(WebentityMixin):
    title = Column(Text)
    page_contents_id = Column(Integer())
    tags = Column(Text)
    parent = Column(String(400), default="")
    publishing_date = Column(DateTime)
    crawling_date = Column(DateTime)

    @classmethod
    def make(cls, item):
        return cls(url=item['url'],
                   title=item['title'],
                   tags=item['tags'],
                   parent=item['parent'],
                   publishing_date=item['publishing_date'],
                   crawling_date=item['crawling_date'])


class Scraps(PageMixin, Base):
    __tablename__ = 'scraps'


class Links(WebentityMixin, Base):
    __tablename__ = 'links'


class Downloads(Base):
    __tablename__ = 'downloads'
    url = Column(String(400), primary_key=True)
    downloaded = Column(Integer(), default=0)


class Contents(Base):
    __tablename__ = 'content'
    id = Column(Integer, primary_key=True)
    page_code = Column(LargeBinary)

    @classmethod
    def make(cls, item):
        return cls(page_code=item['page_code'])


# this generates all tables for declared models
Base.metadata.create_all(engine, checkfirst=True)


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