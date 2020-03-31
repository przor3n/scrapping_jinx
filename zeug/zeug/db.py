#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    MetaData,
    Column,
    Integer,
    Text,
    String,
    DateTime,
    LargeBinary,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from zeug.env import (DB_CONNECTION, DB_SCHEMA)

# this has to be only one
# engine = create_engine('sqlite:///file.db')
engine = create_engine(DB_CONNECTION)

assert engine, 'Engine not set'

Session = sessionmaker(bind=engine)
session = Session()  # use session object

assert session, 'Session not set'

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