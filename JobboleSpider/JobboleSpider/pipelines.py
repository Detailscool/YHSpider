# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline

class JobbolespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class JobboleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        item = super(JobboleImagePipeline, self).item_completed(results, item, info)
        for ok, value in results:
            item['front_image_path'] = value['path']
        return item
