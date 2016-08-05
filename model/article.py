#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Moore.Huang <moore@moorehy.com>


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