# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

from datetime import datetime
import re
from JobboleSpider.utils import common


class JobbolespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class TakeStrEncode(object):
    def __call__(self, values):
        result_values = [value.encode('utf-8') for value in values if isinstance(value, unicode)]
        if not result_values:
            result_values = [value for value in values if isinstance(value, str)]
        return result_values


def date_convert(value):
    try:
        create_date = datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.now().date()

    return create_date


def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


def remove_comment_tags(value):
    # 去掉tag中提取的评论
    if "评论" in value:
        return ""
    else:
        return value

def image_url_value(value):
    if value.startswith('//'):
        value.replace('//', '')
    if not value.startswith('http://'):
        value = 'http://' + value
    return value


def str_encode(value):
    return value.encode('utf-8')

class JobbleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = TakeStrEncode()


class JobboleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field(
        input_processor=MapCompose(common.get_md5)
    )
    front_image_url = scrapy.Field(
        output_processor=MapCompose(image_url_value)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(str_encode, remove_comment_tags),
        output_processor=Join(",")
    )
    content = scrapy.Field(
        output_processor=Join("")
    )

    def get_insert_sql(self):
        insert_sql = """
                      INSERT INTO jobbole(title, url, url_object_id, create_date, fav_nums, tags)
                      VALUES (%s, %s, %s, %s, %s, %s)  ON DUPLICATE KEY UPDATE content=VALUES(fav_nums)
                """
        params = (self['title'], self['url'], self['url_object_id'], self['create_date'], self['fav_nums'], self['tags'])
        return insert_sql, params