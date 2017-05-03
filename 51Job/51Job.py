#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool
import csv
import sys
from pybloomfilter import BloomFilter

reload(sys)
sys.setdefaultencoding('utf-8')

company_bf = BloomFilter(1024*1024*16, 0.01)

def get_company(url, page=1):
    if page > 10:
        print '公司总数 ：', len(company_bf)
        return

    wbdata = requests.get(url).content
    soup = BeautifulSoup(wbdata, 'lxml')
    # print soup.prettify()
    company_list = soup.select('div.el > span.t2')
    # print type(company_list), '\ncompany_list :', company_list
    for index, company in enumerate(company_list):
        if index != 0:
            # print type(company),'company:', company.encode('utf-8')
            company_result = company.find_all(name='a')  #公司名称#
            company_link = company_result[0].attrs['href']
            company_name = company_result[0].attrs['title']# 公司链接#
            print company_name, ' - ', company_link

            if company_link not in company_bf:
                company_bf.add(company_link)
            # print company_link
        # else:
        #     print company.encode('utf-8')

    next_page = soup.select('div.p_in > ul > li.bk')
    next_page_link = next_page[-1].find_all(name='a')[0].attrs['href']
    print 'next_page_link :', next_page_link
    get_company(next_page_link, page+1)


if __name__ == '__main__':
    url = 'http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=030200%2C040000&industrytype=32%2C03%2C62&keywordtype=1&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9'
    get_company(url)

