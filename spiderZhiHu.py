#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Moore.Huang <moore@moorehy.com>

import requests
# import time

headers = {'Host': 'news-at.zhihu.com',
           'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) '
                         'AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}
news = requests.get('http://news-at.zhihu.com/api/4/news/latest', headers=headers)
print news.url, news.status_code
print news.text

