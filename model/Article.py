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

    def init_with_article(self, article):
        self.aid = article.aid
        self.timestamp = article.timestamp
        self.article_id = article.article_id
        self.title = article.title
        self.images = article.images
        self.star = article.star
        self.top = article.top
        self.tags = article.tags

    @staticmethod
    def get_article_obj_with_list(data):
        a = Article()
        a.aid = data[0]
        a.timestamp = data[1]
        a.article_id = data[2]
        a.title = data[3]
        a.images = data[4]
        a.star = data[5]
        a.top = data[6]
        a.tags = data[7]
        return a

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

    def load_with_article_id(self, article_id):
        article = self.__is_article_exits(article_id)
        if article is None:
            Utils.print_log(u'加载文章失败: %s' % article_id, prefix=u'[加载文章对象]')
            sys.exit(1)
        self.init_with_article(article)
        return self

    @staticmethod
    def load_article_list_with_date(date):
        """
        通过日期加载文章列表

        :type date: string 时间字符串, 格式为"YYYYmmdd", 如: 20160813
        """
        def select_article_id(cur, conn):
            count = cur.execute(u"SELECT `article_id` FROM `article` WHERE `timestamp`=%d"
                                % Utils.decode_str_to_time(date))

            article_id_list = []
            if count > 0:
                results = cur.fetchall()
                for r in results:
                    article_id_list.append(r[0])

            conn.commit()
            return ReturnCodeModel(obj=article_id_list)

        rcm = Utils.process_database(select_article_id, u'查询文章ID列表', log=False)
        if not rcm.is_success():
            Utils.print_log(rcm, prefix=u'[查询文章ID列表]')
            sys.exit(1)

        article_list = []
        for a in rcm.obj:
            article_list.append(Article().load_with_article_id(a))
        return article_list

    def __is_article_exits(self, article_id):
        def select_article(cur, conn):
            count = cur.execute(u"SELECT * FROM `article` WHERE `article_id` LIKE '%s'"
                                % article_id)
            article = None
            if count == 1:
                result = cur.fetchone()
                article = self.get_article_obj_with_list(result)

            conn.commit()
            return ReturnCodeModel(obj=article)

        rcm = Utils.process_database(select_article, u'插入文章信息', log=False)
        return rcm.obj

    def insert(self):
        if self.__is_article_exits(self.article_id):
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

        rcm = Utils.process_database(insert_article, u'插入文章信息', log=False)
        return rcm
