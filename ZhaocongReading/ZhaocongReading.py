#!/usr/bin/python
# -*- coding:utf-8 -*-
# ZhaocongReading.py
# Created by Henry on 2017/12/19
# Description : 爬去兆聪读报


from MyBot import get_bot
import time

if __name__ == '__main__':
    time.sleep(30)
    bot = get_bot()
    bot.wechat_name = 'Henry'
    bot.send_news()

