#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Moore.Huang <moore@moorehy.com>

import sys

import requests

from model.Article import Article
from model.Utils import Utils

reload(sys)
sys.setdefaultencoding('utf8')


# TODO 1) 实现抓取当天文章, 并存入DB, DB应包含是否已阅读, 是否感兴趣, 是否TOP, 以及相关TAG(此数据阅读后更新)
# TODO 2) 从DB中取出当天的文章, 生成对应的Bookmarks文件(将[TOP], [D]标志表现在文章title中), 用于导入到浏览器
# TODO 3) 将DB中的文章请求并保存到本地
# TODO 4) 将本地保存的文章生成为mobi文件, 并发送到Kindle


def get_news_by_net(date=None):
    headers = {'Host': 'news-at.zhihu.com',
               'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) '
                             'AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}
    request_url = u'http://news-at.zhihu.com/api/4/news/latest'
    if date:
        request_url = u'http://news.at.zhihu.com/api/4/news/before/%s' % date
    news = requests.get(request_url, headers=headers)
    # print news.url, news.status_code
    # print news.text
    if news.status_code != 200:
        print(u'获取最新文章列表失败: [%s]%s' % (news.status_code, news.text))
        sys.exit(1)
    return news.text


content = get_news_by_net()

news_content = Utils.json_loads(content)
date = Utils.decode_str_to_time(news_content['date'])
Utils.print_log(u'日期时间戳: <%s>%d' % (news_content['date'], date), prefix=u'[测试]')

# 生成文章列表
articles = []
stories_list = news_content['stories']
stories_list.reverse()
for a in stories_list:
    article = Article().init_with_time_and_data(date, a)
    articles.append(article)
    # Utils.print_log(article)

# 从文章列表中提取文章ID列表
article_ids = []
for a in articles:
    article_ids.append(a.article_id)

# 若数据包中包含top_stories字段, 则更新文章列表中对象的TOP属性
if 'top_stories' in news_content:
    top_stories_list = news_content['top_stories']
    top_stories_list.reverse()
    for top in top_stories_list:
        top_article_id = top['id']
        if top_article_id in article_ids:
            for a in articles:
                if top_article_id == a.article_id:
                    a.top = 1
                    break

# 打印文章列表
for a in articles:
    rcm = a.insert()
    if not rcm.is_success():
        Utils.print_log(rcm)
    Utils.print_log(a)
