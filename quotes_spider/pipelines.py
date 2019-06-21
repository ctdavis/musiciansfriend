import MySQLdb.cursors
from twisted.enterprise import adbapi
from pydispatch import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings
import logging
from quotes_spider import settings
from time import sleep

class QuotesSpiderPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def __init__(self, stats):
        connected = False
        retries = 0
        max_retries = 50
        while not connected and retries < max_retries:
            self.dbpool = adbapi.ConnectionPool('MySQLdb',
                host=settings.MYSQL_HOST,
                user=settings.MYSQL_USER,
                passwd=settings.MYSQL_PASS,
                #port=settings.MYSQL_PORT,
                db=settings.MYSQL_DB,
                charset='utf8',
                use_unicode=True,
                cursorclass=MySQLdb.cursors.DictCursor
            )
            try:
                self.dbpool.connect()
                connected = True
            except Exception as e:
                self._handle_error(e)
            finally:
                retries += 1
            
        self.stats = stats
        dispatcher.connect(self.spider_closed, signals.spider_closed)
            

    def spider_closed(self, spider):
        self.dbpool.close()
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._insert_record, item)
        query.addErrback(self._handle_error)
        return item
    def _insert_record(self, tx, item):
        fields = ['quote', 'author']
        values = ['"'+item[field]+'"' for field in fields]
        result = tx.execute(
            """ INSERT INTO quotes ({}) VALUES ({}) """\
            .format(','.join(fields), ','.join(values))
        )
        if result > 0:
            self.stats.inc_value('database/items_added')
    def _handle_error(self, e):
        logging.error(e)
