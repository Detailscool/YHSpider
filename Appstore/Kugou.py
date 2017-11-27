#!/usr/bin/python
# -*- coding:utf-8 -*-
#  Kugou.py
#  Created by HenryLee on 2017/10/23.
#  Copyright © 2017年. All rights reserved.
#  Description : 爬取Kugou的AppStore言论

import requests
import json
import csv
import sys
import codecs
import time

reload(sys)
sys.setdefaultencoding('utf-8')

appid = 472208016
# startIndex = 0
# endIndex = 100
step = 100

for i in range(1000):
    url = 'https://itunes.apple.com/WebObjects/MZStore.woa/wa/userReviewsRow?cc=cn&id=%d&displayable-kind=11&startIndex=%d&endIndex=%d&sort=0&appVersion=all' % (appid, step*i, step*(i+1))
    headers = {'User-Agent': 'iTunes/11.0 (Windows; Microsoft Windows 7 Business Edition Service Pack 1 (Build 7601)) AppleWebKit/536.27.1'}
    res = requests.get(url=url, headers=headers)
    # print res.content

    res_dict = json.loads(res.content)
    user_review_list = res_dict["userReviewList"]

    f = codecs.open('./result/%d-%d.csv' % (step*i, step*(i+1)), 'wb', 'utf-8')
    # writer = csv.writer(f)
    # writer.writerow(['date', 'userReviewId', 'title', 'body', 'rating'])

    # ratings = []
    for user_review in user_review_list:
        # ratings.append(int(user_review['rating']))
        # writer.writerow([user_review['date'], user_review['userReviewId'], user_review['title'], user_review['body'].replace('\n', '').replace(' ', ''), user_review['rating']])
        f.write('\t'.join([user_review['date'].encode('utf-8'), str(user_review['userReviewId']), user_review['title'].encode('utf-8'), user_review['body'].encode('utf-8').replace('\n', '').replace(' ', ''), str(user_review['rating'])])+'\n')

    f.close()

    print '%d-%d -> Done' % (step*i, step*(i+1))

    time.sleep(1)

# import matplotlib.pyplot as plt
# print ratings
# print list(set(ratings))
# plt.xlim(0, 6)
# plt.hist(ratings, normed=True)
# plt.show()
