#!/usr/bin/python
# -*- coding:utf-8 -*-
# main.py
# Created by Henry on 2017/11/6
# Description :

from KugouBot import get_bot
from KugouMeal import KugouMeal
from KugouMealConfig import KugouMealConfig
import time
import sys

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print '请输入账号密码'
        sys.exit()

    login_name = sys.argv[1]
    login_password = sys.argv[2]

    config = KugouMealConfig()

    selected_dict = config.get_meal_dict()
    wechat_name = config.get_wechat_name()

    while True:
        skipSeconds = config.get_skip_seconds()

        print 'skipSeconds ：', skipSeconds

        if skipSeconds > 60 * 45:
            time.sleep(skipSeconds)

        time.sleep(20)

        if not config.has_ordered():
            print 'Begin 点餐'

            kugou_meal = KugouMeal(login_name, login_password, selected_dict)
            selected_restaurant, selected_meal = kugou_meal.start()

            config.update_date()
            config.update_order(selected_restaurant, selected_meal)

            print '已经选餐'

            time.sleep(20)

            if get_bot() is not None:
                print '入来了'
                get_bot().send_msg(wechat_name, '已帮您随机点餐，今天是：\n%s - %s' % (selected_restaurant, selected_meal))
            else:
                print '无入来'

        else:
            print '已经选餐'

        time.sleep(60*45)
