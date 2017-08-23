# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
from datetime import datetime

import codecs
import json
import sys
import MySQLdb
import MySQLdb.cursors

reload(sys)
sys.setdefaultencoding('utf8')

class JobbolespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常
        return item

    def handle_error(self, failure, item, spider):
        #处理异步插入的异常
        print failure

    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        # insert_sql, params = item.get_insert_sql()
        insert_sql = """
                    INSERT INTO jobbole(title, url, url_object_id, create_date, fav_nums)
                    VALUES (%s, %s, %s, %s, %s)
        """
        date = datetime.strptime(item['create_date'], '%Y/%m/%d').date()
        params = (item['title'], item['url'], item['url_object_id'], date, item['fav_nums'])
        cursor.execute(insert_sql, params)

class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('jobbole.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        item_dict = dict(item)
        lines = json.dumps(item_dict) + '\n'
        self.file.write(lines)
        return item
    def spider_closed(self, spider):
        self.file.close()

class JsonExpoerterPipeline(object):
    def __init__(self):
        self.file = open('jobboleexpoter.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

class JobboleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        item = super(JobboleImagePipeline, self).item_completed(results, item, info)
        for ok, value in results:
            item['front_image_path'] = value['path']
        return item
