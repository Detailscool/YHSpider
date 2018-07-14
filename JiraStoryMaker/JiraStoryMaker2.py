#!/usr/bin/python
# -*- coding:utf-8 -*-
# JiraStoryMaker.py
# Created by Henry on 2018/4/9
# Description :

import time
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import os
import json

reload(sys)
sys.setdefaultencoding('utf-8')


def create_story(**kwargs):
    summary_text = kwargs.get('summary_text', None)
    work_time_text = kwargs.get('work_time_text', None)
    REQ = kwargs.get('REQ', None)

    new_button = driver.find_element_by_id('create_link')
    new_button.click()
    time.sleep(0.5)

    drop_menus = driver.find_elements_by_class_name('aui-ss-icon')

    project = drop_menus[0]
    project.click()

    data_suggestions = driver.find_element_by_id('project-options').get_attribute('data-suggestions')
    items = json.loads(data_suggestions)
    # print items
    if isinstance(items, list) and items and isinstance(items[0], dict) and isinstance(items[0]['items'], list) and items[0]['items'] and isinstance(items[0]['items'][0], dict) and items[0]['items'][0]['label']:
        select_group = items[0]['items'][0]['label']
        if u'IOSZHIBO' not in select_group:
            groups = [a for a in driver.find_elements_by_css_selector('li a.aui-list-item-link') if 'IOSZHIBO' in a.text]
            # print '\ngroups:', groups
            if groups:
                groups[0].click()
                print 'click'
                time.sleep(0.5)
        else:
            project.click()

    story_type = driver.find_element_by_id('issuetype-single-select')
    story_type.click()
    story_type_groups = [a for a in driver.find_elements_by_css_selector('li a.aui-list-item-link') if u'故事'==a.text]
    if story_type_groups:
        story_type_groups[0].click()
        time.sleep(0.5)

    drop_menus = driver.find_elements_by_class_name('aui-ss-icon')
    if len(drop_menus) < 5:
        time.sleep(10)
        print '出错啦'
        sys.exit(1)

    summary = driver.find_element_by_id('summary')
    summary.send_keys(unicode(summary_text))
    time.sleep(0.5)

    sprint = drop_menus[4]
    sprint.click()
    sprint_groups = [a for a in driver.find_elements_by_css_selector('li a.aui-list-item-link') if u'iOS直播服务组' in a.text]
    if sprint_groups:
        sprint_groups[0].click()
        time.sleep(0.5)

    test_type = Select(driver.find_element_by_id('customfield_10200'))
    test_type.select_by_value('10200')
    time.sleep(0.5)

    requestment = Select(driver.find_element_by_id('customfield_10101'))
    requestment.select_by_value('10101')
    time.sleep(0.5)

    work_time = driver.find_element_by_id('customfield_10833')
    work_time.send_keys(work_time_text)

    # code = driver.find_element_by_id('customfield_10503-3')
    # code.click()

    if REQ:
        question = driver.find_element_by_id('issuelinks-issues-textarea')
        question.send_keys(unicode(REQ))

    items = driver.find_elements_by_css_selector('li.menu-item')
    if items and len (items) > 1:
        relationship_item = items[1]
        relationship_item.click()
        time.sleep(0.5)

        dev_person = driver.find_element_by_css_selector('#customfield_10300_container textarea')
        if dev_person and login_token.split('-'):
            dev_person.send_keys(login_token.split('-')[0])
            time.sleep(0.5)

    submit = driver.find_element_by_id('create-issue-submit')
    submit.click()
    time.sleep(2)

    story = driver.find_element_by_css_selector('#aui-flag-container div div a')
    story_href = story.get_attribute('href')
    print summary_text, ': ', story_href
    # print '已建: ', summary_text, ', 时长， :', work_time_text, '天'


if __name__ == '__main__':
    login_token = sys.argv[1]
    file_path = sys.argv[2]

    if not os.path.exists(file_path):
        print '出错啦'
        sys.exit(1)
    else:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            f.close()

    if '-' not in login_token:
        print '出错啦'
        sys.exit(1)
    elif len(login_token.split('-')[-1]) != 32:
        print '出错啦'
        sys.exit(1)

    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)

    url = '' + login_token

    driver.get(url)
    # print driver.get_cookies()

    for line in lines:
        if '，' in line and ',' not in line:
            words = line.encode('utf-8').strip().split('，')
        elif ',' in line and '，' not in line:
            words = line.encode('utf-8').strip().split(',')
        else:
            words = []

        if len(words) == 2:
            create_story(summary_text=words[0].strip(), work_time_text=words[1].strip())
        elif len(words) == 3:
            create_story(summary_text=words[0].strip(), work_time_text=words[1].strip(), REQ=words[2].strip())

    driver.close()