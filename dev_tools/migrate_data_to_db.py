#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Moore.Huang <moore@moorehy.com>

import logging
import os
import re
import sys

# 准备Django环境
from django.core.wsgi import get_wsgi_application

DJANGO_PROJECT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'server')
print(DJANGO_PROJECT_PATH)
sys.path.append(DJANGO_PROJECT_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
application = get_wsgi_application()

# 导入Django工程相关模块
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from articles.models import *
from terms import models as terms_models

# 初始化logger
logger_format = '%(asctime)s [%(name)s][%(filename)s:%(lineno)d]' \
                '[%(levelname)s] %(message)s'
logging.basicConfig(
    level=logging.INFO,
    format=logger_format)
logger = logging.getLogger('Tool')

# 业务常量
_matches = lambda l, r: any([r.search(l)])
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
METADATA_RE = re.compile(r'^\(.*\);|,$')


def migrate_tags_data():
    """
    将原article应用中的Tag模型数据迁移到Terms应用中的term&taxonomy模型中
    """
    tags = Tag.objects.all()
    cnt_term = 0
    cnt_taxonomy = 0
    for tag in tags:
        logger.info('[处理]标签 => {}'.format(tag.theme))
        term, created = terms_models.Term.objects.get_or_create(
            name=tag.theme,
            slug=tag.theme)
        if created:
            term.save()
            cnt_term += 1
        taxonomy, created = terms_models.Taxonomy.objects.get_or_create(
            term=term,
            taxonomy_type='post_tag')
        if created:
            taxonomy.save()
            cnt_taxonomy += 1
    logger.info('共处理标签条目：{}, 分类条目：{}'.format(cnt_term, cnt_taxonomy))


# 条目数据迭代生成
def yield_item_data(page_html_store_path):
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
            src = Source.objects.get(name='zhihu_daily')
        except models.ObjectDoesNotExist:
            src = Source.objects.create(name='zhihu_daily', author='小貘', verbose_name='知乎日报',
                                        description='每天三次，每次七分钟。在中国，资讯类移动应用的人均阅读时长是 5 分钟，而在知乎日报，这个数字是 21')

        tag_list = []
        if any([self.tags]):
            for tag in self.tags.split(','):
                try:
                    t = Tag.objects.get(theme=tag)
                except models.ObjectDoesNotExist:
                    t = Tag.objects.create(theme=tag, creator=user)
                tag_list.append(t)

        url = 'http://daily.zhihu.com/story/{}'.format(self.article_id)
        pub_datetime = timezone.datetime.fromtimestamp(float(self.timestamp), tz=timezone.get_current_timezone())
        try:
            article = Article.objects.get(url=url)
            article.pub_datetime = pub_datetime
            article.title = self.title
            article.source = src
            article.cover_image = self.imgs
            article.save()
        except models.ObjectDoesNotExist:
            article = Article.objects.create(pub_datetime=pub_datetime,
                                             title=self.title, source=src,
                                             cover_image=self.imgs,
                                             url=url)

        try:
            zhihu = ZhihuDaily.objects.get(article=article)
            zhihu.daily_id = self.article_id
            zhihu.top = self.top
            zhihu.save()
        except models.ObjectDoesNotExist:
            zhihu = ZhihuDaily.objects.create(article=article, daily_id=self.article_id, top=self.top)

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
migrate_tags_data()
