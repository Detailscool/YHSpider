#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv
import sys
import datetime
from time import time
from pybloomfilter import BloomFilter

reload(sys)
sys.setdefaultencoding('utf-8')

download_bf = BloomFilter(1024*1024*16, 0.01)

def request(url, isFirstPage):
    if url not in download_bf:
        download_bf.add(url)
    else:
        return

    res = requests.get(url).text
    soup = BeautifulSoup(res, 'html.parser')
    # print soup.prettify()

    keylist = soup.select('div.key-list > div.item-mod')
    for index, house in enumerate(keylist):
        # if index == 2:
            # print house

        house_name = house.find_all(name='a', class_='items-name') #房子名称#

        house_link = house_name[0].attrs['href'] #房子链接#
        # print house_link

        if house_name:
            house_name = house_name[0].text
            # print house_name

        house_status = ''
        house_status_forSale = house.find_all(name='i', class_='status-icon forsale') #房子代售#
        if house_status_forSale:
            house_status = house_status_forSale[0].text
            # print house_status_forSale

        house_status_onSale = house.find_all(name='i', class_='status-icon onsale') #房子在售#
        if house_status_onSale:
            house_status = house_status_onSale[0].text
            # print house_status_onSale

        house_status_soldOut = house.find_all(name='i', class_='status-icon soldout') #房子售罄#
        if house_status_soldOut:
            house_status = house_status_soldOut[0].text
            # print house_status_onSale

        house_address = house.find_all(name='a', class_='list-map') #房子地址#
        sub_district = ''
        if house_address:
            house_address = house_address[0].text
            sub_district = house_address[house_address.find('[') + 1: house_address.find(']')].strip()
            sub_district = sub_district[sub_district.find(' ') + 1: ]
            house_address = house_address[house_address.find(']') + 1:].strip()
            # print house_address
            # print house_address[0].text
            # print sub_district, len(sub_district)

        house_type = house.find_all(name='p') #户型#
        for i, t in enumerate(house_type):
            if not t.attrs:
                if type(t.a) is not type(None):
                    b = t.find_all(name='a')
                    str = ''
                    for types in b:
                        str += types.text + ' '
                    house_type = str.strip()
                    # print house_type
                elif type(t) is not type(None):
                        house_type = t.text
                # print house_type
                break
            if i == len(house_type) - 1:
                house_type = None

        price_txt = house.find_all(name='p', class_='price-txt') #价格描述#
        if price_txt:
            price_txt = price_txt[0].string
            # print price_txt
        else:
            price_txt = ''

        house_price = ''
        price = house.find_all(name='p', class_='price') #均价#
        if price:
            house_price = u'均价' + price[0].span.text + '元/㎡'
            # print price

        price_undetermined = house.find_all(name='p', class_='favor-tag around-price') #周边均价#
        if price_undetermined:
            house_price = u'周边均价' + price_undetermined[0].span.text + '元/㎡'
            # print price_undetermined

        tel = house.find_all(name='p', class_='tel') #销售电话#
        if tel :
            tel = tel[0].text
            # print tel
        else:
            tel = ''

        dynamic = house.find_all(name='div', class_='data-brief') #动态描述#
        if dynamic and dynamic[0].em.text.encode('utf-8') == u'动态：'.encode('utf-8'):
            dynamic = dynamic[0].a.text
            # print dynamic
        else:
            dynamic = ''

        writer.writerow([district_name, sub_district, house_name, house_status, house_address, house_type, price_txt, house_price, dynamic, tel, house_link])

    if isFirstPage:
        pages_select = soup.select('div.pagination')
        for pages in pages_select:
            page = pages.find_all(name='a')
            for i in range(len(page)):
                next_url = page[i].attrs['href']  # , '\n', page
                request(next_url, False)

if __name__ == '__main__':

    begin = time()

    f = open(u'佛山楼盘%s.csv' % (datetime.datetime.now().strftime('%Y%m%d')), 'wb')
    f.write(unicode('\xEF\xBB\xBF', 'utf-8'))
    writer = csv.writer(f)
    writer.writerow(['区域', '子区域', '楼盘名称', '楼盘状态', '楼盘地址', '户型', '价格描述', '价格', '动态描述', '销售电话', '楼盘链接'])

    url_main = 'http://fs.fang.anjuke.com/'

    res = requests.get(url_main).text
    soup = BeautifulSoup(res, 'html.parser')
    # print soup.prettify()

    districts = soup.select('div.filter > a')
    # print districts

    for index, district in enumerate(districts):
        url = district.attrs['href']
        district_name = district.string
        # if index == 0:
        request(url, True)

        # print '%s - %s' % (district_name, url)
        # # if index == 0:
        # res = requests.get(url).text
        # soup = BeautifulSoup(res, 'html.parser')
        # # if index == 1:
        # # print soup.prettify()
        #
        # pages_select = soup.select(r'div.pagination')
        # # print pages_select.a[0].attrs['href']
        # for i, pages in enumerate(pages_select):
        #     page = pages_select[0].find_all(name='a')
        #     print len(page)
        #     print page
        #     print i
    print '用时 ：', time() - begin