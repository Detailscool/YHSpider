#!/usr/bin/python
# -*- coding:utf-8 -*-
#  main.py
#  Created by HenryLee on 2017/9/14.
#  Copyright © 2017年. All rights reserved.
#  Description :

from scrapy.cmdline import execute

'''
billtopall_spider
billtopar_spider
billtopcountry_spider
billtopedm_spider
billtoprap_spider
billtoprap_spider2
billtoprb_spider
billtoprock_spider
billtopsong_spider
'''

execute(['scrapy', 'crawl', 'billtopsong_spider'])