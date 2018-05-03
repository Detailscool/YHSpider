#!/usr/bin/python
# -*- coding:utf-8 -*-
# JiraStoryMaker.py
# Created by Henry on 2018/4/9
# Description :

import time
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import Select


reload(sys)
sys.setdefaultencoding('utf-8')


def create_story(summary_text, work_time_text, req_text):
    new_button = driver.find_element_by_id('create_link')
    new_button.click()

    time.sleep(0.5)

    inputs = driver.find_elements_by_class_name('drop-menu')
    if len(inputs) < 6:
        sys.exit(1)

    project = inputs[0]
    project.click()
    time.sleep(0.5)

    data_suggestions = driver.find_element_by_id('project-options').get_attribute('data-suggestions')
    import json
    items = json.loads(data_suggestions)
    if isinstance(items, list) and items and isinstance(items[0], dict) and isinstance(items[0]['items'], list) and items[0]['items'] and isinstance(items[0]['items'][0], dict) and items[0]['items'][0]['label']:
        select_group = items[0]['items'][0]['label']
        if u'IOSZHIBO' not in select_group:
            groups = [a for a in driver.find_elements_by_css_selector('li a.aui-list-item-link') if 'IOSZHIBO' in a.text]
            if groups:
                groups[0].click()
                time.sleep(0.5)

    summary = driver.find_element_by_id('summary')
    summary.send_keys(unicode(summary_text))
    time.sleep(0.5)

    sprint = inputs[5]
    sprint.click()
    sprint_groups = [a for a in driver.find_elements_by_css_selector('li a.aui-list-item-link') if u'手机iOS直播服务组' in a.text]
    if sprint_groups:
        sprint_groups[0].click()
        time.sleep(0.5)

    requestment = Select(driver.find_element_by_id('customfield_10101'))
    requestment.select_by_value('10101')
    time.sleep(0.5)

    work_time = driver.find_element_by_id('customfield_10833')
    work_time.send_keys(work_time_text)
    time.sleep(0.5)

    code = driver.find_element_by_id('customfield_10503-3')
    code.click()

    question = driver.find_element_by_id('issuelinks-issues-textarea')
    question.send_keys(unicode(req_text))

    submit = driver.find_element_by_id('create-issue-submit')
    submit.click()


if __name__ == '__main__':
    login_name = sys.argv[1]
    login_password = sys.argv[2]

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    url = 'http://opd.kugou.net/common/signinApi.php?appId=v1-59f840241db88&url=http%3A%2F%2Fj.fxwork.kugou.net%2Fsecure%2FViewProfile.jspa'

    driver.get(url)
    name = driver.find_element_by_id('userName')
    password = driver.find_element_by_id('userPwd')
    loginbutton = driver.find_element_by_xpath('/html/body/form/div[2]/div[4]/button')
    name.send_keys(login_name)
    password.send_keys(login_password)
    loginbutton.click()
    time.sleep(0.5)

    print driver.current_url

    if login_name.lower() not in url:
        print '账号密码不对'
        sys.exit(1)
    # print driver.get_cookies()

    create_story('396家乐福建安路空间发的', '1', 'REQ-930')