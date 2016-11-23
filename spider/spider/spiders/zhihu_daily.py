# -*- coding: utf-8 -*-
import json
import time

import scrapy
from django.db import models
from scrapy.selector import Selector
from spider.items import ArticleItem
from spider.items import SourceItem

from articles.models import ZhihuDaily


class ZhihuDailySpider(scrapy.Spider):
    # 来源名称，唯一，长度<50，用于文章源模型索引创建后不可修改
    name = "zhihu_daily"

    # 组件作者
    author = "小貘"

    # 显示名称，长度<100，Spider每次运行时更新
    verbose_name = "知乎日报"

    # 描述信息，长度<255，Spider每次运行时更新
    description = "每天三次，每次七分钟。在中国，资讯类移动应用的人均阅读时长是 5 分钟，而在知乎日报，这个数字是 21"

    allowed_domains = ["zhihu.com"]
    start_urls = (
        'http://news-at.zhihu.com/api/4/news/latest',
    )

    def __init__(self, *a, **kw):
        super(ZhihuDailySpider, self).__init__(*a, **kw)
        self.datetime = None

        # 此参数为当前Spider爬取数据持久化时的指定子路径，
        # 需在item流入pipeline前设置，格式采用：`spider.name`/`yyyy-mm-dd`，如：zhihu_daily/2016-11-22
        self.persistent_path = ''
        self.source = SourceItem(name=self.name, author=self.author, verbose_name=self.verbose_name,
                                 description=self.description).save_to_db()

    def parse(self, response):
        return self.yield_article_request(response=response)

    def yield_article_request(self, response):
        content_raw = response.body.decode()
        self.logger.debug('响应body原始数据：{}'.format(content_raw))
        content = json.loads(content_raw, encoding='UTF-8')
        self.logger.debug(content)

        self.datetime = time.strptime(content['date'], "%Y%m%d")

        # 设置persistent_path，即爬取数据经过Pipeline持久化时使用的存储路径
        strftime = time.strftime("%Y-%m-%d", self.datetime)
        self.logger.info('日期：{}'.format(strftime))
        self.persistent_path = '{}/{}'.format(self.name, strftime)

        if 'top_stories' in content:
            self.logger.info('处理头条文章')
            for item in content['top_stories']:
                for story in content['stories']:
                    if item['id'] == story['id']:
                        story['top'] = True
                        break
                self.logger.debug(item)

        self.logger.info('处理今日文章')
        for item in content['stories']:
            self.logger.info(item)

            # 从DB中查询该日报文章ID是否已存在，存在则忽略，不存在继续执行后续逻辑
            z = ZhihuItem(daily_id=item['id'], top=item.get('top', False))
            if z.exists(spider=self):
                self.logger.warn('该文章已存在于DB，丢弃：《{}》'.format(item['title']))
                continue

            # 初步填充ArticleItem数据
            a = ArticleItem()
            a['pub_datetime'] = self.datetime
            a['source'] = self.source
            a['addition_info'] = z

            url = 'http://news-at.zhihu.com/api/4/news/{}'.format(z['daily_id'])
            request = scrapy.Request(url, callback=self.parse_article)
            request.meta['item'] = a
            yield request

    def parse_article(self, response):
        content = json.loads(response.body.decode(), encoding='UTF-8')
        a = response.meta['item']

        # 继续填充ArticleItem数据
        a['title'] = content['title']
        a['url'] = content['share_url']
        a['cover_image'] = content.get('image', content.get('images', [None])[0])
        a['content'] = content['body']
        self.logger.debug(a)

        # 为图片持久化pipeline执行做数据准备
        a['image_urls'] = [a['cover_image']]

        # 格式化content，将其中的img标签src全部导出到image_urls中
        a['image_urls'] += Selector(text=a['content']).css('img::attr(src)').extract()
        self.logger.debug('待处理的图片url(过滤前): {}'.format(a['image_urls']))

        # 过滤掉image_urls中的公式url，目前未找到好方法将其转换为图片持久化
        a['image_urls'] = [img for img in a['image_urls'] if 'equation?tex=' not in img]
        self.logger.debug('待处理的图片url: {}'.format(a['image_urls']))
        yield a


class ZhihuItem(scrapy.Item):
    daily_id = scrapy.Field()  # 日报文章ID
    top = scrapy.Field()  # 热文标志

    def save_to_db_by_article(self, article, spider):
        try:
            zhihu = ZhihuDaily.objects.get(article=article)
            zhihu.daily_id = self.get('daily_id')
            zhihu.top = self.get('top')
            zhihu.save()
        except models.ObjectDoesNotExist:
            zhihu = ZhihuDaily.objects.create(article=article, daily_id=self.get('daily_id'),
                                              top=self.get('top'))

    def exists(self, spider):
        try:
            zhihu = ZhihuDaily.objects.get(daily_id=self.get('daily_id'))
            spider.logger.info('测试文章是否存在: {}'.format(self.get('daily_id')))
            return True
        except models.ObjectDoesNotExist:
            return False
