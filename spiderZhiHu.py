#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Moore.Huang <moore@moorehy.com>

import sys
import json
import requests
# import time

# TODO 1) 实现抓取当天文章, 并存入DB, DB应包含是否已阅读, 是否感兴趣, 是否TOP, 以及相关TAG(此数据阅读后更新)
# TODO 2) 从DB中取出当天的文章, 生成对应的Bookmarks文件(将[TOP], [D]标志表现在文章title中), 用于导入到浏览器
# TODO 3) 将DB中的文章请求并保存到本地
# TODO 4) 将本地保存的文章生成为mobi文件, 并发送到Kindle

headers = {'Host': 'news-at.zhihu.com',
           'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) '
                         'AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}
news = requests.get('http://news-at.zhihu.com/api/4/news/latest', headers=headers)
# print news.url, news.status_code
# print news.text
if news.status_code != 200:
    print(u'获取最新文章列表失败: [%s]%s' % (news.status_code, news.text))
    sys.exit(1)


class Utils(object):
    @staticmethod
    def json_loads(raw):
        return json.loads(raw, encoding="UTF-8")

    @staticmethod
    def json_dumps(raw):
        return json.dumps(raw, indent=None, encoding="UTF-8", ensure_ascii=False)