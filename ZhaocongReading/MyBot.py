#!/usr/bin/python
# -*- coding:utf-8 -*-
# KugouBot.py
# Created by Henry on 2017/11/6
# Description :

# import sys
# sys.path.append('../WXBot/')
# print sys.path

from threading import Thread
from wxbot import *
from bs4 import BeautifulSoup
import requests


class MyBot(WXBot):

    _instance = None

    wechat_name = ''

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(MyBot, cls).__new__(cls, *args, **kw)
        return cls._instance

    def handle_msg_all(self, msg):
        if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
            print msg
            self.send_msg_by_uid(self.get_message(), msg['user']['id'])

            # if msg[]

    def run_bot(self):
        self.DEBUG = True
        self.conf['qr'] = 'png'
        self.run()

    def __del__(self):
        print 'Bot挂了'


    def get_message(self):
        url = 'https://712383.kuaizhan.com/'
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'lxml')
        link = soup.select('.no-pic a')[0]
        new_url = url + link['href'][1:]
        # print new_url
        # print soup.prettify()

        res = requests.get(new_url)
        soup = BeautifulSoup(res.content, 'lxml')
        content = soup.select('.mp-content p')
        result = ''
        for a in content:
            result += a.get_text() + '\n\n'
        return result.strip()

    def send_news(self):
        message = self.get_message()
        self.send_msg(self.wechat_name, message)

def run_bot():
    global bot
    bot = MyBot()
    bot.run_bot()


def get_bot():
    global bot
    # print bot.contact_list
    return bot


global bot
t = Thread(target=run_bot)
t.start()
