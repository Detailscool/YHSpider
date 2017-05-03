#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool
import csv
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def get_zhaopin(page):
    url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=全国&kw=机器学习&p={0}&kt=3'.format(page)
    print("第{0}页".format(page))
    wbdata = requests.get(url).content
    soup = BeautifulSoup(wbdata,'lxml')
    # if page == 1:
    #     print soup.prettify()

    job_name = soup.select("table.newlist > tr > td.zwmc > div > a")
    salarys = soup.select("table.newlist > tr > td.zwyx")
    locations = soup.select("table.newlist > tr > td.gzdd")
    times = soup.select("table.newlist > tr > td.gxsj > span")
    links = soup.select('table.newlist > tr > td.gsmc > a')

    for name, salary, location, time, link in zip(job_name, salarys, locations, times, links):
        writer.writerow([name.get_text(), salary.get_text(), time.get_text(), location.get_text(), link.attrs['href']])

if __name__ == '__main__':
    job_title = u'机器学习'

    f = open(u'智联招聘%s岗位.csv' % (job_title), 'wb')
    f.write(unicode('\xEF\xBB\xBF', 'utf-8'))
    writer = csv.writer(f)
    writer.writerow(['公司名称', '薪水', '时间', '位置', '链接'])

    url = r'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=全国&kw=%s&p=1&kt=3' % (job_title)
    wbdata = requests.get(url).content
    soup = BeautifulSoup(wbdata, 'lxml')
    # print soup.prettify()
    # print str(soup)

    items = soup.select("div#newlist_list_content_table > table")
    # print items[1]
    count = len(items) - 1
    # 每页职位信息数量
    print count

    job_count = re.findall(r'共<em>(.*?)</em>个职位满足条件', str(soup))[0]
    print job_count
    # 搜索结果页数
    pages = (int(job_count) // count) + 1
    # print pages

    pool = Pool(processes=2)
    pool.map_async(get_zhaopin, range(1, pages + 1))
    pool.close()
    pool.join()