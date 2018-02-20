#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Moore.Huang <moore@moorehy.com>

import logging
import os
import sys
from bs4 import BeautifulSoup

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
from posts import models as posts_models
from spiders import models as spiders_models

# 初始化logger
logger_format = '%(asctime)s [%(name)s][%(filename)s:%(lineno)d]' \
                '[%(levelname)s] %(message)s'
logging.basicConfig(
    level=logging.INFO,
    format=logger_format)
logger = logging.getLogger('Tool')


def migrate_tags_data():
    """
    将原articles应用中的Tag模型数据迁移到Terms应用中的term&taxonomy模型中
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


def migrate_articles_data(page_html_store_path):
    """
    迁移原articles应用中的article/zhihudaily模型数据
    """
    # 验证传入路径文件是否存在
    if not os.path.exists(page_html_store_path):
        raise ValueError()

    # 读取数据库article模型获取到所有待处理数据条
    articles = Article.objects.filter(
        pub_datetime__gt=timezone.datetime(2017, 7, 21)
    ).order_by('pub_datetime', 'id')
    spider, created = spiders_models.Spider.objects.get_or_create(
        name='zhihu_daily',
        display_name='知乎日报',
        defaults={
            'author': '小貘',
            'email': 'moore@moorehy.com',
            'description': '每天三次，每次七分钟。在中国，资讯类移动应用的人均阅'
                           '读时长是 5 分钟，而在知乎日报，这个数字是 21'
        })
    spider.save()

    cnt_article = 0
    cnt_postmeta = 0
    cnt_readrecord = 0
    cnt_relation = 0
    for a in articles:
        content = ''
        logger.info('[处理]文章 => [{}][{}]{}'. format(
            a.id, a.pub_datetime, a.title))
        if a.url_local:
            url = os.path.join(page_html_store_path, a.url_local)
            with open(url, 'r') as p:
                content = p.read()
                soup = BeautifulSoup(content, "lxml")
                content = str(soup.div)
                # logger.info('[{url}]{content}'.format(
                #     url=a.url,
                #     content=content))

        # 文章数据填充
        post, created = posts_models.Post.objects.get_or_create(
            origin_url=a.url,
            defaults={
                'spider': spider,
                'date': a.pub_datetime,
                'content': content,
                'title': a.title,
                'modified': a.pub_datetime
            })
        if created:
            post.date = a.pub_datetime
            post.modified = a.pub_datetime
            post.save()
            post.date = a.pub_datetime
            post.save()
            cnt_article += 1

        # 通用元数据字段填充
        postmeta, created = posts_models.PostMeta.objects.get_or_create(
            post=post,
            name='moear.page_slug_local',
            defaults={
                'value': a.url_local and a.url_local.split('/')[-1] or ''
            })
        if created:
            postmeta.save()
            cnt_postmeta += 1
        postmeta, created = posts_models.PostMeta.objects.get_or_create(
            post=post,
            name='moear.cover_image_slug',
            defaults={
                'value': a.cover_image or ''
            })
        if created:
            postmeta.save()
            cnt_postmeta += 1
        value = a.cover_image_local and a.cover_image_local.split('/')[-1]
        value = value or ''
        postmeta, created = posts_models.PostMeta.objects.get_or_create(
            post=post,
            name='moear.cover_image_slug_local',
            defaults={
                'value': value,
            })
        if created:
            postmeta.save()
            cnt_postmeta += 1

        # 知乎日报爬虫特有元数据字段填充
        try:
            zhihudaily = ZhihuDaily.objects.get(article=a)
            postmeta, created = posts_models.PostMeta.objects.get_or_create(
                post=post,
                name='spider.zhihu_daily.id',
                defaults={
                    'value': zhihudaily.daily_id
                })
            if created:
                postmeta.save()
                cnt_postmeta += 1
            postmeta, created = posts_models.PostMeta.objects.get_or_create(
                post=post,
                name='spider.zhihu_daily.top',
                defaults={
                    'value': 1 if zhihudaily.top else 0
                })
            if created:
                postmeta.save()
                cnt_postmeta += 1
        except ZhihuDaily.DoesNotExist:
            pass

        try:
            # 阅读记录数据迁移
            readrecord = ReadRecord.objects.get(reader=user, article=a)
            rr, created = posts_models.ReadRecord.objects.get_or_create(
                post=post,
                user=user,
                defaults={
                    'star': readrecord.star,
                    'comment': readrecord.comment or '',
                })
            if created:
                rr.save()
                cnt_readrecord += 1

            # 分类数据迁移
            tags = [tag for tag in Tag.objects.filter(readrecord=readrecord)]
            for tag in tags:
                taxonomy = terms_models.Taxonomy.objects.get(
                    term=terms_models.Term.objects.get(slug=tag.theme))
                relation, created = \
                    terms_models.Relationships.objects.get_or_create(
                        post=post,
                        taxonomy=taxonomy,
                        user=user)
                if created:
                    relation.save()
                    cnt_relation += 1
        except ReadRecord.DoesNotExist:
            pass

        # sys.exit(0)
    logger.info('共处理文章条目：{}, 文章元数据：{}, 阅读记录：{}, 分类：{}'.format(
        cnt_article, cnt_postmeta, cnt_readrecord, cnt_relation))


def update_taxonomy_count():
    cnt = 0
    taxonomys = terms_models.Taxonomy.objects.all()
    for tax in taxonomys:
        count_his = tax.count
        tax.count = terms_models.Relationships.objects.filter(
            taxonomy=tax).count()
        if tax.count != count_his:
            tax.save()
            cnt += 1
    logger.info('共更新了标签文章技术信息：{}'.format(cnt))


"""
# migrate data to db

## 功能说明
此脚本为将 `V0.2.0` 版本中已爬取的数据文件填充入新创建的Django相应数据模型中

## 准备数据
在V0.2.0版本的MySQL数据库中，导出article表得到 `.sql` 文件，放入 `./data` 路径下

## 需配置参数
1. username 迁移数据时某些数据条目需设置创建人/阅读人等V1.0.0版本中不存在的字段，此处统一设置
2. page_html_store_path 页面HTML文件所在基路径
"""
username = 'moore'
page_html_store_path = '/Volumes/Warehouse/backup/'

user = User.objects.get(username=username)
migrate_tags_data()
migrate_articles_data(page_html_store_path)
update_taxonomy_count()
