#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Moore.Huang <moore@moorehy.com>

import sys

import requests

from Article import Article
from Browser import Browser
from Utils import Utils


class Zhihu(object):
    def __init__(self):
        self.date_str = u''
        self.articles = []
        self.article_ids = []

    @staticmethod
    def __get_news_by_net(date=None):
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

    def spider_articles_from_net(self, date=None):
        content = self.__get_news_by_net(date)

        news_content = Utils.json_loads(content)
        self.date_str = news_content['date']
        date = Utils.decode_str_to_time(self.date_str)
        Utils.print_log(u'日期时间戳: <%s>%d' % (news_content['date'], date), prefix=u'[测试]')

        # 生成文章列表
        self.articles = []
        stories_list = news_content['stories']
        stories_list.reverse()
        for a in stories_list:
            article = Article().init_with_time_and_data(date, a)
            self.articles.append(article)
            # Utils.print_log(article)

        # 从文章列表中提取文章ID列表
        self.article_ids = []
        for a in self.articles:
            self.article_ids.append(a.article_id)

        # 若数据包中包含top_stories字段, 则更新文章列表中对象的TOP属性
        if 'top_stories' in news_content:
            top_stories_list = news_content['top_stories']
            top_stories_list.reverse()
            for top in top_stories_list:
                top_article_id = top['id']
                if top_article_id in self.article_ids:
                    for a in self.articles:
                        if top_article_id == a.article_id:
                            a.top = 1
                            break

        for a in self.articles:
            rcm = a.insert()
            if not rcm.is_success():
                Utils.print_log(rcm)

    def spider_articles_html(self, date, path=None):
        """
        通过日期加载文章列表并保存到指定路径下

        :type date: str
        :type path: str
        :param date: 时间字符串, 格式为"YYYYmmdd", 如: 20160813
        :param path: 保存文章的根路径
        """
        # 抓取文章html页并保存到指定的路径下
        self.articles = Article().load_article_list_with_date(date)
        Browser(path).save_web_with_articles(self.articles)

    def print_articles(self):
        # 打印文章列表
        if len(self.articles) == 0:
            Utils.print_log(u'文章列表内容为空!', prefix=u'[打印文章列表]')
            sys.exit(1)
        for a in self.articles:
            Utils.print_log(a)
        Utils.print_log(u'共打印%d篇文章' % len(self.articles), prefix=u'[打印文章列表]')
