#!/usr/bin/python
# -*- coding:utf-8 -*-
#  DoubanHot.py
#  Created by HenryLee on 2017/9/25.
#  Copyright © 2017年. All rights reserved.
#  Description :


import warnings

warnings.filterwarnings("ignore")
import jieba  # 分词包
import numpy  # numpy计算包
import codecs  # codecs提供的open方法来指定打开的文件的语言编码，它会在读取的时候自动转换为内部unicode
import re
import pandas as pd
import matplotlib.pyplot as plt
import urllib2
from bs4 import BeautifulSoup as bs
import matplotlib
matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)
from wordcloud import WordCloud  # 词云包
import sys
import numpy as np
import requests

reload(sys)
sys.setdefaultencoding('utf8')

# 分析网页函数
def getNowPlayingMovie_list():
    url = 'https://movie.douban.com/nowplaying/guangzhou/'

    # request = urllib2.Request(url)
    # request.add_header('Upgrade-Insecure-Requests', '1')
    # request.add_header('User-Agent',
    #                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')
    # request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    # request.add_header('Accept-Encoding', 'gzip,deflate,sdch')
    # request.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')
    s = requests.session()
    html_data = s.get(url, headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}, verify=False, proxies={'http': 'http://122.193.14.102:80'}).text

    # response = urllib2.urlopen(request)
    # html_data = response.read().decode('utf-8')
    soup = bs(html_data, 'html.parser')
    nowplaying_movie = soup.find_all('div', id='nowplaying')
    nowplaying_movie_list = nowplaying_movie[0].find_all('li', class_='list-item')
    nowplaying_list = []
    for item in nowplaying_movie_list:
        nowplaying_dict = {}
        nowplaying_dict['id'] = item['data-subject']
        for tag_img_item in item.find_all('img'):
            nowplaying_dict['name'] = tag_img_item['alt']
            nowplaying_list.append(nowplaying_dict)
    return nowplaying_list


# 爬取评论函数
def getCommentsById(movieId, pageNum):
    eachCommentList = []
    if pageNum > 0:
        start = (pageNum - 1) * 20
    else:
        return False
    requrl = 'https://movie.douban.com/subject/' + movieId + '/comments' + '?' + 'start=' + str(start) + '&limit=20'
    print requrl
    resp = urllib2.urlopen(requrl)
    html_data = resp.read().decode('utf-8')
    soup = bs(html_data, 'html.parser')
    comment_div_lits = soup.find_all('div', class_='comment')
    for item in comment_div_lits:
        if item.find_all('p')[0].string is not None:
            eachCommentList.append(item.find_all('p')[0].string)
    return eachCommentList


def main():
    # 循环获取第一个电影的前10页评论
    commentList = []
    NowPlayingMovie_list = getNowPlayingMovie_list()
    for i in range(1):
        num = i + 1
        commentList_temp = getCommentsById(NowPlayingMovie_list[0]['id'], num)
        commentList.append(commentList_temp)

    # # 将列表中的数据转换为字符串
    comments = ''
    for k in range(len(commentList)):
        a = commentList[k]
        comments = comments + ''.join(commentList[k]).strip()

    # 使用正则表达式去除标点符号
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    filterdata = re.findall(pattern, comments.encode())
    # filterdata = [word.encode().replace('\\', '') for word in list(set(filterdata))]
    print filterdata[:10]
    cleaned_comments = ''.join(filterdata)

    # 使用结巴分词进行中文分词
    segment = jieba.lcut(cleaned_comments.encode())
    print segment[:10]
    segment = [unicode(word) for word in segment]
    segment = list(set(segment))
    words_df = pd.DataFrame({'segment': segment})

    # 去掉停用词
    f = open('stopwords.txt')
    # data = [line.encode('utf-8').strip() for line in f.readlines() if isinstance(line, unicode)]
    data = []
    for line in f.readlines():
        data.append(line.strip())
    f.close()
    # data = np.loadtxt('stopwords.txt', delimiter='\n', dtype=str)
    # stopwords = pd.read_csv("stopwords.txt", index_col=False, quoting=3, sep="\n", names=['stopword'], encoding='utf-8') # quoting=3全不引用
    stopwords = pd.DataFrame(data, columns=['stopword'])
    words_df = words_df[~words_df.segment.isin(stopwords.stopword)]

    # 统计词频
    words_stat = words_df.groupby(by=['segment'])['segment'].agg({"计数": numpy.size})
    words_stat = words_stat.reset_index().sort_values(by=["计数"], ascending=False)

    # 用词云进行显示
    wordcloud = WordCloud(font_path="simhei.ttf", background_color="white", max_font_size=80)
    word_frequence = {x[0]: x[1] for x in words_stat.head(1000).values}

    word_frequence_list = []
    for key in word_frequence:
        key = key.encode('utf-8')
        temp = (key, word_frequence[key])
        word_frequence_list.append(temp)

    wordcloud = wordcloud.fit_words(word_frequence_list)
    plt.imshow(wordcloud)


# 主函数
main()