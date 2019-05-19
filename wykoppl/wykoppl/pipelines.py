# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from wykoppl.db import session
from wykoppl.items import LinkItem, DownloadedItem, Scraps, Links
from datetime import datetime
#from logging import logging

class WykopplPipeline(object):

    choices = {
        DownloadedItem: 'process_page',
        LinkItem: 'process_link'
    }

    def process_item(self, item, spider):
        function_name = self.choices.get(type(item), 'empty')

        getattr(self, function_name)(item)

        return item

    def empty(self, item):
        print("dupa") #logging.error('Something is empty in pipeline')
        pass

    def process_link(self, link_item):
        link = Links.make(link_item)

        url = link.url
        link_in_db = session.query(Links).filter_by(url=url).first()

        if not link_in_db:
            session.add(link)
            session.commit()

        pass

    def process_page(self, downloaded_item):
        now = datetime.now()
        downloaded_item['crawling_date'] = now

        page = Scraps.make(downloaded_item)

        url = page.url
        link_in_db = session.query(Links).filter_by(url=url).first()

        if not link_in_db:
            session.add(page)
            session.commit()

        pass
