#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Moore.Huang <moore@moorehy.com>

import sys

from model.Utils import Utils
from model.Zhihu import Zhihu

reload(sys)
sys.setdefaultencoding('utf8')

# TODO 1) 实现抓取当天文章, 并存入DB, DB应包含是否已阅读, 是否感兴趣, 是否TOP, 以及相关TAG(此数据阅读后更新)
# TODO 2) 从DB中取出当天的文章, 生成对应的Bookmarks文件(将[TOP], [D]标志表现在文章title中), 用于导入到浏览器
# TODO 3) 将DB中的文章请求并保存到本地
# TODO 4) 将本地保存的文章生成为mobi文件, 并发送到Kindle


zhihu = Zhihu()
zhihu.spider_articles_from_net()
zhihu.print_articles()
