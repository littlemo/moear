#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Moore.Huang <moore@moorehy.com>

import sys

from ReturnCodeModel import ReturnCodeModel
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

    def __str__(self):
        top_str = u'[   ]'
        if self.top:
            top_str = u'[TOP]'
        return u'<%s>[%d][%5s]%s%s|%s' % (Utils.encode_time_to_str(self.timestamp),
                                          self.article_id, u'*' * self.star, top_str, self.title,
                                          self.images.split(','))

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

    def __is_article_exits(self):
        def select_article(cur, conn):
            count = cur.execute(u"SELECT * FROM `article` WHERE `article_id` LIKE '%s'"
                                % self.article_id)
            conn.commit()
            return ReturnCodeModel(obj=count)

        rcm = Utils.process_database(select_article, u'插入文章信息')
        return bool(rcm.obj)

    def insert(self):
        if self.__is_article_exits():
            return ReturnCodeModel(ReturnCodeModel.Code_Duplicate, u'目标文章ID(%s)已存在于DB无法插入' % self.article_id)

        def insert_article(cur, conn):
            count = cur.execute(u"INSERT INTO `mo_zhihu_daily`.`article` (`id`, `timestamp`, `article_id`, `title`, "
                                u"`images`, `star`, `top`, `tags`) "
                                u"VALUES (NULL, '%d', '%d', '%s', '%s', '%d', '%d', NULL)"
                                % (self.timestamp, self.article_id, self.title, self.images, self.star, self.top))
            if count != 1:
                return ReturnCodeModel(ReturnCodeModel.Code_Bad_Database_Process,
                                       u'插入文章信息异常: 结果不为一(%d)' % count)
            conn.commit()
            return ReturnCodeModel()

        rcm = Utils.process_database(insert_article, u'插入文章信息')
        return rcm
