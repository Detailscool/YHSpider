#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
from JobCrawler import JobCrawler
from pybloomfilter import BloomFilter
from time import time

company_bf = BloomFilter(1024*1024*16, 0.01)
total_page = 1

def get_company_info(url, page=1):
    if page > total_page:
        return

    wbdata = requests.get(url).content
    soup = BeautifulSoup(wbdata, 'lxml')
    # print soup.prettify()
    company_list = soup.select('div.el > span.t2')
    # print type(company_list), '\ncompany_list :', company_list
    for index, company in enumerate(company_list):
        if index != 0:
            company_result = company.find_all(name='a')
            company_link = company_result[0].attrs['href']
            company_name = company_result[0].attrs['title']
            print company_name, ' - ', company_link

            if company_link not in company_bf:
                company_bf.add(company_link)
                # if index < 3:
                crawler = JobCrawler()
                crawler.get_job_info(company_link)
            # print company_link
        # else:
        #     print company.encode('utf-8')

    next_page = soup.select('div.p_in > ul > li.bk')
    next_page_link = next_page[-1].find_all(name='a')[0].attrs['href']
    print 'next_page_link :', next_page_link
    get_company_info(next_page_link, page+1)

if __name__ == '__main__':
    start = time()

    url = 'http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=030200%2C040000&industrytype=32%2C03%2C62&keywordtype=1&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9'
    get_company_info(url)

    print '总共 %s 间公司, 共 %s 页，总耗时：%s' % (len(company_bf), total_page, time() - start)

