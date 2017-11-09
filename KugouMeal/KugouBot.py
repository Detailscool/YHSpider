#!/usr/bin/python
# -*- coding:utf-8 -*-
# KugouBot.py
# Created by Henry on 2017/11/6
# Description :

from threading import Thread
from wxbot import *


class KugouBot(WXBot):

    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(KugouBot, cls).__new__(cls, *args, **kw)
        return cls._instance

    def handle_msg_all(self, msg):
        if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
            print msg
            self.send_msg_by_uid(u'hi', msg['user']['id'])

    def run_bot(self):
        self.DEBUG = True
        self.conf['qr'] = 'png'
        self.run()


def run_bot():
    global bot
    bot = KugouBot()
    bot.run_bot()


def get_bot():
    global bot
    # print bot.contact_list
    return bot


global bot
t = Thread(target=run_bot)
t.start()
