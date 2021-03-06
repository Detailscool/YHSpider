#!/usr/bin/python
# -*- coding:utf-8 -*-
#  KugouMeal.py
#  Created by HenryLee on 2017/10/27.
#  Copyright © 2017年. All rights reserved.
#  Description :

from selenium import webdriver
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent
import random
import sys


class KugouMeal(object):
    def __init__(self, login_name, login_password, selected_dict):
        self.login_name = login_name
        self.login_password = login_password
        self.selected_dict = selected_dict

        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def get_random_meal(self):
        selected_restaurant = random.choice(self.selected_dict.keys())
        selected_meal = random.choice(self.selected_dict[selected_restaurant])
        return selected_restaurant, selected_meal

    url = ''

    def select_meal(self):
        selected_restaurant, selected_meal = self.get_random_meal()

        # print BeautifulSoup(driver.page_source, 'html.parser').prettify()
        restaurants_eles = self.driver.find_elements_by_css_selector('#restaurantLinks1 a')
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        restaurants = soup.select('#restaurantLinks1 a')
        if len(restaurants) == len(restaurants_eles):
            for restaurant, ele in zip(restaurants, restaurants_eles):
                # print restaurant.get_text()
                if restaurant.get_text().encode('utf-8').strip() == selected_restaurant:
                    ele.click()
                    time.sleep(1)

                    book_buttons = self.driver.find_elements_by_css_selector('table tbody tr td')
                    soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                    tds = soup.select('table tbody tr td')
                    for i in range(1, len(tds), 5):
                        if selected_meal in tds[i].get_text().encode('utf-8').strip():
                            book_button = book_buttons[i + 3].find_elements_by_css_selector('input')
                            book_button[0].click()
                            return True, selected_restaurant, selected_meal
                            # print tds[i].get_text()
                    break
        return False, None, None

    def start(self):
        self.driver.get(self.url)

        login_field = self.driver.find_element_by_id('userName')
        password_field = self.driver.find_element_by_id('userPwd')
        login_button = self.driver.find_element_by_xpath('//*[@id="login_tab_content"]/div[1]/div[3]/button')

        if login_field and password_field and login_button:
            login_field.send_keys(self.login_name)
            password_field.send_keys(self.login_password)
            login_button.click()

            time.sleep(2)

            meal_url = self.driver.current_url
            if self.login_name.lower() not in meal_url:
                print '账号密码不对'
                sys.exit(1)

            while True:
                has_selected, selected_restaurant, selected_meal = self.select_meal()
                if has_selected and selected_restaurant and selected_meal:
                    return selected_restaurant, selected_meal
                self.driver.get(meal_url)

    def __del__(self):
        self.driver.close()
