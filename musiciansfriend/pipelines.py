# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb.cursors
from twisted.enterprise import adbapi

from pydispatch import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings
import logging

SETTINGS = get_project_settings()

class MusiciansfriendPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def __init__(self, stats):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            host=SETTINGS['MYSQL_HOST'],
            user=SETTINGS['MYSQL_USER'],
            passwd=SETTINGS['MYSQL_PASS'],
            port=SETTINGS['MYSQL_PORT'],
            db=SETTINGS['MYSQL_DB'],
            charset='utf8',
            use_unicode=True,
            cursorclass=MySQLdb.cursors.DictCursor
        )
        self.stats = stats
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        self.dbpool.close()

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._insert_record, item)
        query.addErrback(self._handle_error)
        return item

    def _insert_record(self, tx, item):
        fields = ['url','style','price','availability','name','brand']
        values = ['"'+item[field]+'"' for field in fields]
        result = tx.execute(
            """ INSERT INTO musiciansfriend ({}) VALUES ({})"""\
            .format(','.join(fields),','.join(values))
        )
        if result > 0:
            self.stats.inc_value('database/items_added')

    def _handle_error(self, e):
        logging.error(e)
