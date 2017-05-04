#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
import requests
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

    driver = webdriver.PhantomJS()
    f = open(u'前程无忧%s.csv' % (datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')), 'wb')
    f.write(unicode('\xEF\xBB\xBF', 'utf-8'))
    writer = csv.writer(f)
    writer.writerow(['公司', '公司性质', '公司人数', '行业', '职位', '学历', '区域', '薪酬', '发布时间', '链接'])
    current_company = ''

    def get_job(self, soup):
        start = time.time()

        # print 'soup.prettify :', soup.prettify()

        company_name = soup.select('div.in > h1')
        company_scale = soup.select('div.in > p.ltype')
        company_info = []
        for name, scale in zip(company_name, company_scale):
            name = name.get_text()
            if self.current_company != name:
                self.current_company = name
                company_info.append(name)
                for a in scale.get_text().split('|'):
                    company_info.append(a.strip())
        if company_info:
            self.writer.writerow(company_info)
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
                self.writer.writerow(['', '', '', '', title.get_text(), degree.get_text(), area.get_text(), salary.get_text(),distribute_time.get_text(), title.attrs['href']])

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
            next = self.driver.find_elements_by_link_text('下一页')
            # print 'next: ', next, len(next)
            if next:
                next[-1].click()
                time.sleep(1)
                bs = BeautifulSoup(self.driver.page_source, 'lxml')
                self.get_job(bs)

    def get_job_info(self, url):
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
        }

        self.driver.get(url)

        wbdata = requests.get(url, headers=header)
        wbdata.encoding ='gb18030'
        soup = BeautifulSoup(wbdata.text, 'html.parser')
        self.get_job(soup)

# Test
# a = JobCrawler()
# a.get_job_info('http://jobs.51job.com/all/co3456551.html')
# a.get_job_info('http://jobs.51job.com/all/co3688655.html')