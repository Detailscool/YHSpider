#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import re

def get_job_info():
    start = time.time()

    job_list = soup.select('div.dw_table')
    # print 'job_list ：', job_list
    for job in job_list:
        job_titles = job.find_all(name='a', class_='zw-name')
        job_degrees = job.find_all(name='span', class_='t2')
        job_areas = job.find_all(name='span', class_='t3')
        job_salaries = job.find_all(name='span', class_='t4')
        job_time = job.find_all(name='span', class_='t5')
        for title, degree, area, salary, distribute_time in zip(job_titles, job_degrees, job_areas, job_salaries, job_time):
            print title.get_text(), '-', degree.get_text(), '-', area.get_text(), '-', salary.get_text(), '-',distribute_time.get_text(), '-', title.attrs['href']

    current_page = soup.select('li.on')[-1]
    current_page = int(current_page.get_text())
    next_page = soup.select('li.bk > a')[0].attrs['href']
    next_page = int(re.findall('\d+', next_page)[-1])

    print current_page, '-', next_page, '-', (current_page==next_page)

    print '耗时：', time.time() - start

if __name__ == '__main__':
    url = r'http://jobs.51job.com/all/co3919935.html'

    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
    }

    wbdata = requests.get(url, headers=header).content
    soup = BeautifulSoup(wbdata, 'lxml')
    print soup.prettify()

    get_job_info()


