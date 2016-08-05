#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Moore.Huang <moore@moorehy.com>

import sys

from Utils import Utils


class Article(object):
    def __init__(self):
        self.aid = 0
        self.timestamp = 0
        self.article_id = 0
        self.title = u''
        self.images = u''  # 若为多个图片, 则以','分隔
        self.star = 0
        self.top = 0
        self.tags = u''  # 若为多个tag, 则以','分隔

    def init_with_time_and_data(self, timestamp, data):
        self.timestamp = timestamp
        try:
            self.article_id = data['id']
            self.title = data['title']
            self.images = ','.join(data['images'])
        except Exception as e:
            Utils.print_log(u'初始化解析data字典异常: %s' % e, prefix=u'[Err]')
            sys.exit(1)
        return self
