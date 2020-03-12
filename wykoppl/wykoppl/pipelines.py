# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from wykoppl.db import session
from wykoppl.items import LinkItem, DownloadedItem, Scraps, Links, Downloads
from datetime import datetime
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import InvalidRequestError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound

class WykopplPipeline(object):

    choices = {
        DownloadedItem: 'process_page',
        LinkItem: 'process_link'
    }

    def process_item(self, item, spider):
        if 'page_code' in item:
            self.process_page(item)
        else:
            self.process_link(item)

        return item

    def empty(self, item):
        print("dupa") #logging.error('Something is empty in pipeline')
        pass

    def process_link(self, link_item):
        link = Links.make(link_item)

        try:
            session.add(link)
            session.commit()
        except IntegrityError:
            session.rollback()
        except InvalidRequestError:
            session.rollback()
        except Exception as e:
            session.rollback()
            raise e

        pass

    def process_page(self, downloaded_item):
        now = datetime.now()
        downloaded_item['crawling_date'] = now

        page = Scraps.make(downloaded_item)

        try:
            logitem = session.query(Downloads).filter(Downloads.url == page.url).one()
            logitem.downloaded = 1
        except NoResultFound:
            logitem = Downloads(url=page.url, downloaded = 1)
        except Exception as e:
            raise e

        try:
            session.add(page)
            session.add(logitem)
            session.commit()

        except IntegrityError:
            session.rollback()
        except InvalidRequestError:
            session.rollback()
        except Exception as e:
            session.rollback()
            raise e

        pass
