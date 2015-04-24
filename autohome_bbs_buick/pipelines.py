# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log
from datetime import datetime
from twisted.enterprise import adbapi

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class AutohomeBbsBuickPipeline(object):

    words_to_filter = ['买']

    def process_item(self, item, spider):

        for word in self.words_to_filter:
            if word in unicode(item['content']):
                print item['content']

        return item

class MySqlStorePipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWD'],
            charset = 'utf8',
            use_unicode = True
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)

        return cls(dbpool)

    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        d.addErrback(self._handler_error, item, spider)
        d.addBoth(lambda _: item)
        return d


    def _do_upsert(self, conn, item, spider):
        # now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        conn.execute('''
            INSERT INTO autohome_bbs_content (title, content, pub_time, author, author_url, reg_time, addr, attent_vehicle)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (item['title'], item['content'], item['pub_time'], item['author'],
              item['author_url'], item['reg_time'], item['addr'], item['attent_vehicle']))

    def _handler_error(self, failure, item, spider):
        log.err(failure)

