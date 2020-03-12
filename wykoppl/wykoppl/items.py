# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from sqlalchemy.ext.declarative import declarative_base
from wykoppl.db import engine
from sqlalchemy import (MetaData,
                        Column,
                        Integer,
                        Text, String,
                        DateTime,
                        LargeBinary,)

from wykoppl.env import DB_SCHEMA

meta = MetaData(schema=DB_SCHEMA)

Base = declarative_base(metadata=meta)


class WebentityMixin:
     id = Column(Integer, primary_key=True)
     url = Column(Text)

     @classmethod
     def make(cls, item):
          return cls(url=item['url'])


class PageMixin(WebentityMixin):
     title = Column(Text)
     page_contents_id = Column(Integer())
     tags = Column(Text)
     publishing_date = Column(DateTime)
     crawling_date = Column(DateTime)

     @classmethod
     def make(cls, item):
          return cls(url=item['url'],
              title=item['title'],
              tags=item['tags'],
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


class DownloadedItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    tags = scrapy.Field()
    page_code = scrapy.Field()
    publishing_date = scrapy.Field()
    crawling_date = scrapy.Field()
