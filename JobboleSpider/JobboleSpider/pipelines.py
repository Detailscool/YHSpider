# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter

import codecs
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')

class JobbolespiderPipeline(object):
    def process_item(self, item, spider):
        return item

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
