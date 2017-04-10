#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import json

if __name__ == '__main__':
    url = 'http://www.toutiao.com/api/pc/focus/'
    wbdata = requests.get(url).text

    data = json.loads(wbdata)
    news = data['data']['pc_feed_focus']

    for n in news:
        title = n['title'].encode('utf-8')
        img_url = n['image_url'].encode('utf-8')
        url = n['media_url'].encode('utf-8')
        print title, ',', img_url, ',', url

