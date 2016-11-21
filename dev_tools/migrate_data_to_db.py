#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Moore.Huang <moore@moorehy.com>

import logging
import os
import re
import sys

# 准备Django环境
from django.core.wsgi import get_wsgi_application

DJANGO_PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DJANGO_PROJECT_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moear.settings")
application = get_wsgi_application()

# 导入Django工程相关模块
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from articles.models import *

# 初始化logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(name)s][%(filename)s:%(lineno)d][%(levelname)s] %(message)s')
logger = logging.getLogger('Tool')

# 业务常量
_matches = lambda l, r: any([r.search(l)])
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
METADATA_RE = re.compile(r'^\(.*\);|,$')


# 条目数据迭代生成
def yield_item_data(sql_file_path):
    sql = os.path.abspath(sql_file_path)
    logger.info('sql文件路径: {}'.format(sql))

    # 验证传入路径文件是否存在
    if not os.path.exists(sql):
        return None

    # 读取文件并通过Re获取到所有待处理数据条
    with open(sql, 'r') as s:
        cnt_record = 0
        lines = s.readlines()
        for l in lines:
            if _matches(l, METADATA_RE):
                cnt_record += 1
                l = l.strip()
                logger.debug(l)
                yield l
        logger.info('共处理记录条目：{}'.format(cnt_record))


# 条目数据格式化模型
class ItemFormatter(object):
    RE = re.compile(r"^\((\d+), (\d+), (\d+), '(.+)', '(.+)', (\d+), (\d+), ('(.+)'|NULL), ('(.+)'|NULL)\)[,;]$")

    def __init__(self, item):
        raw = self.RE.match(item)
        groups = raw.groups()
        logger.debug(groups)
        self.timestamp = float(groups[1])
        self.article_id = int(groups[2])
        self.title = groups[3]
        self.imgs = groups[4]
        self.star = int(groups[5])
        self.top = groups[6]
        self.tags = groups[8]
        self.comment = groups[10]

    def save_to_db(self):
        try:
            src = Source.objects.get(name='知乎日报')
        except models.ObjectDoesNotExist:
            src = Source.objects.create(name='知乎日报')

        tag_list = []
        if any([self.tags]):
            for tag in self.tags.split(','):
                try:
                    t = Tag.objects.get(theme=tag)
                except models.ObjectDoesNotExist:
                    t = Tag.objects.create(theme=tag, creater=user)
                tag_list.append(t)

        url = 'http://daily.zhihu.com/story/{}'.format(self.article_id)
        pub_datetime = timezone.datetime.fromtimestamp(float(self.timestamp), tz=timezone.get_current_timezone())
        try:
            article = Article.objects.get(url=url)
            article.pub_datetime = pub_datetime
            article.title = self.title
            article.source = src
            article.save()
        except models.ObjectDoesNotExist:
            article = Article.objects.create(pub_datetime=pub_datetime,
                                             title=self.title, source=src,
                                             url=url)

        try:
            zhihu = ZhihuDaily.objects.get(article=article)
            zhihu.daily_id = self.article_id
            zhihu.cover_image = self.imgs
            zhihu.top = self.top
            zhihu.save()
        except models.ObjectDoesNotExist:
            zhihu = ZhihuDaily.objects.create(article=article, daily_id=self.article_id,
                                              cover_images=self.imgs, top=self.top)

        if any([self.star, self.comment]):
            logger.debug('star: {}, comment: {}, any: {}'.format(self.star, self.comment,
                                                                 any([self.star, self.comment])))
            try:
                read_record = ReadRecord.objects.get(reader=user, article=article)
                read_record.star = self.star
                read_record.comment = self.comment
            except models.ObjectDoesNotExist:
                read_record = ReadRecord.objects.create(reader=user, article=article,
                                                        star=self.star, comment=self.comment)
            read_record.tags = tag_list
            read_record.save()

        return self


"""
# migrate data to db

## 功能说明
此脚本为将 `V1.0.0` 版本中已爬取的数据文件填充入Django相应数据表中

## 准备数据
在V1.0.0版本的MySQL数据库中，导出article表得到 `.sql` 文件，放入 `./data` 路径下

## 需配置参数
1. username 迁移数据时某些数据条目需设置创建人/阅读人等V1.0.0版本中不存在的字段，此处统一设置
2. sql_path_name 从旧版导出的SQL文件路径名，使用相对路径，相对当前文件的目录
"""
username = 'moore'
sql_path_name = 'data/article.sql'

user = User.objects.get(username=username)
sql_path = os.path.join(BASE_DIR, sql_path_name)
cnt_item = 0
for item in yield_item_data(sql_path):
    cnt_item += 1
    item_formatter = ItemFormatter(item).save_to_db()
    logger.info('迁移文章数据：[{:5d}]{}'.format(cnt_item, item_formatter.title))
