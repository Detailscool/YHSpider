#!/usr/bin/python
# -*- coding:utf-8 -*-
# main2.py
# Created by Henry on 2018/2/6
# Description :

from KugouMeal import KugouMeal
from KugouMealConfig import KugouMealConfig
import sys

if __name__ == '__main__':
    login_name = sys.argv[1]
    login_password = sys.argv[2]

    config = KugouMealConfig()

    selected_dict = config.get_meal_dict()

    if not config.has_ordered():
        if login_name and login_password:
            print 'Begin 点餐'

            kugou_meal = KugouMeal(login_name, login_password, selected_dict)
            selected_restaurant, selected_meal = kugou_meal.start()

            config.update_date()
            config.update_order(selected_restaurant, selected_meal)

    else:
        print '已经点餐'