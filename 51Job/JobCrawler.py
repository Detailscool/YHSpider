#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import csv
import sys
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

class JobCrawler(object):
    _instance = None
    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(JobCrawler, cls).__new__(cls, *args, **kw)
        return cls._instance

    __driver = webdriver.PhantomJS()

    __f = open(u'前程无忧%s.csv' % (datetime.datetime.now().strftime('%Y%m%d%H%M%S')), 'wb')
    __f.write(unicode('\xEF\xBB\xBF', 'utf-8'))
    __writer = csv.writer(__f)
    __writer.writerow(['公司', '公司性质', '公司人数', '行业', '职位', '学历', '区域', '薪酬', '发布时间', '链接'])

    __current_company = ''

    def __get_job(self, soup):
        start = time.time()

        # print 'soup.prettify :', soup.prettify()

        company_name = soup.select('div.in > h1')
        company_scale = soup.select('div.in > p.ltype')
        company_info = []
        for name, scale in zip(company_name, company_scale):
            name = name.get_text()
            if self.__current_company != name:
                self.__current_company = name
                company_info.append(name)
                for a in scale.get_text().split('|'):
                    company_info.append(a.strip())
        if company_info:
            self.__writer.writerow(company_info)
        # return

        job_list = soup.select('div.dw_table')
        # print 'job_list ：', job_list
        for job in job_list:
            job_titles = job.find_all(name='a', class_='zw-name')
            job_degrees = job.find_all(name='span', class_='t2')
            job_areas = job.find_all(name='span', class_='t3')
            job_salaries = job.find_all(name='span', class_='t4')
            job_time = job.find_all(name='span', class_='t5')
            for title, degree, area, salary, distribute_time in zip(job_titles, job_degrees, job_areas, job_salaries, job_time):
                # print title.get_text(), '-', degree.get_text(), '-', area.get_text(), '-', salary.get_text(), '-',distribute_time.get_text(), '-', title.attrs['href']
                self.__writer.writerow(['', '', '', '', title.get_text(), degree.get_text(), area.get_text(), salary.get_text(), distribute_time.get_text(), title.attrs['href']])

        current_page = soup.select('li.on')
        next_page = soup.select('li.bk > a')

        if not current_page or not next_page:
            print 'soup出错'
            return

        current_page = int(current_page[-1].get_text())
        next_page = next_page[-1].attrs['href']
        next_page = int(re.findall('\d+', next_page)[-1])

        print current_page, '-', next_page, '-', (current_page==next_page)
        print '耗时：', time.time() - start

        if current_page==next_page:
            return
        else:
            next = self.__driver.find_elements_by_link_text('下一页')
            # print 'next: ', next, len(next)
            if next:
                next[-1].click()
                time.sleep(0.5)
                bs = BeautifulSoup(self.__driver.page_source, 'lxml')
                self.__get_job(bs)

    def get_job_info(self, url):
        self.__driver.get(url)

        soup = BeautifulSoup(self.__driver.page_source, 'html.parser')
        self.__get_job(soup)

# Test
# a = JobCrawler()
# a.get_job_info('http://jobs.51job.com/all/co3456551.html')
# a.get_job_info('http://jobs.51job.com/all/co3688655.html')