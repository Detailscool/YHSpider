#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    # cookie = '''UM_distinctid=15b3c3debef665-0537941edddf5-1d396853-13c680-15b3c3debf09e1; cisession=927cedc3368ef3642aa8f5a4fcb916f6fa20c0f1; CNZZDATA1000201968=237985065-1491360396-null%7C1491371262; Hm_lvt_f805f7762a9a237a0deac37015e9f6d9=1491364343,1491364573,1491372252,1491372262; Hm_lpvt_f805f7762a9a237a0deac37015e9f6d9=1491372900'''
    # header = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    #     'Connection': 'keep-alive',
    #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #     'Cookie': cookie}
    # url = 'https://kankandou.com/book/view/22353.html'
    # wbdata = requests.get(url, headers=header).text
    # soup = BeautifulSoup(wbdata, 'lxml')
    # print(soup)

    cookie = {
        'UM_distinctid': '15b3c3debef665-0537941edddf5-1d396853-13c680-15b3c3debf09e1',
        'cisession': '927cedc3368ef3642aa8f5a4fcb916f6fa20c0f1',
        'CNZZDATA1000201968': '237985065-1491360396-null%7C1491371262',
        'Hm_lvt_f805f7762a9a237a0deac37015e9f6d9': '1491364343, 1491364573, 1491372252, 1491372262',
        'Hm_lpvt_f805f7762a9a237a0deac37015e9f6d9': '1491372900'
    }

    url = 'https://kankandou.com/book/view/22353.html'
    wbdata = requests.get(url, cookies=cookie).text
    soup = BeautifulSoup(wbdata, 'lxml')
    print(soup)

    