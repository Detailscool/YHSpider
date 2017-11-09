#!/usr/bin/python
# -*- coding:utf-8 -*-
# KugouMealConfig.py
# Created by Henry on 2017/11/7
# Description :

import ConfigParser
from datetime import datetime


class KugouMealConfig(object):

    config = ConfigParser.ConfigParser()

    def get_wechat_name(self):
        return self.__get_config('wechat', 'sendtoname')

    def get_meal_dict(self):
        meal_dict = {}
        self.config.read('conf.ini')
        if self.config.has_section('meal'):
            for item, value in self.config.items('meal'):
                meal_dict[item] = value.split(',')
        return meal_dict

    def get_skip_seconds(self):
        order_time = self.__get_config('order', 'ordertime')
        order_hour_minute = order_time.split(':')

        deadline_time = self.__get_config('order', 'deadline')
        deadline_hour_minute = deadline_time.split(':')

        curTime = datetime.now()
        desTime = curTime.replace(hour=int(order_hour_minute[0]), minute=int(order_hour_minute[1]))
        deadlineTime = curTime.replace(hour=int(deadline_hour_minute[0]), minute=int(deadline_hour_minute[1]))
        if desTime.isoweekday() > 5:
            desTime = desTime.replace(day=desTime.day + desTime.isoweekday() - 5)
        delta = desTime - curTime
        skipSeconds = int(delta.total_seconds())
        if skipSeconds < -int((deadlineTime - desTime).total_seconds()):
            skipSeconds += 24 * 60 * 60
        return skipSeconds

    def update_date(self):
        if not self.has_ordered():
            self.__update_config('latestupdate', date=datetime.now().strftime('%Y-%m-%d'))

    def update_order(self, selected_restaurant, selected_meal):
        self.__update_config('ordermeal', meal=selected_restaurant+' - '+selected_meal)

    def has_ordered(self):
        date_str = self.__get_config('latestupdate', 'date')
        now = datetime.now().strftime('%Y-%m-%d')
        return date_str == now

    def __get_config(self, section, item):
        self.config.read('conf.ini')
        for _section in self.config.sections():
            if _section == section:
                for _item, value in self.config.items(section):
                    if _item == item:
                        return value


    def __update_config(self, section, **kwargs):
        file_name = 'conf.ini'
        self.config.read(file_name)
        for _section in self.config.sections():
            if _section == section:
                for key, value in kwargs.items():
                    self.config.set(section, key, value)
        self.config.write(open(file_name, 'r+'))

