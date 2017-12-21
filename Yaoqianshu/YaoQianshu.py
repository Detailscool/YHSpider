#!/usr/bin/python
# -*- coding:utf-8 -*-
# YaoQianshu.py
# Created by Henry on 2017/12/20
# Description : 爬取摇钱树

import requests
from bs4 import BeautifulSoup

url = 'http://www.moneytree33.com/front/invest/investHome2'
res = requests.get(url)
soup = BeautifulSoup(res.content, 'lxml')
# print soup.prettify()

rate_amount = soup.find_all(name='div', class_='item red')
progress_per = soup.select('.progress-per')

# print rate_amount

rate = [rate_amount[i].get_text().encode('utf-8').strip() for i in range(0, len(rate_amount), 2)]
amount = [rate_amount[i].get_text().encode('utf-8').strip() for i in range(1, len(rate_amount), 2)]
progress_per = [i.get_text().encode('utf-8') for i in progress_per]
print rate, len(rate)
print amount, len(amount)
print progress_per, len(progress_per)