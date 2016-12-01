# -*- coding: utf-8 -*-
import datetime
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

    # TODO 增加一个初始化参数，即该参数为True，进行文章源Source的插入&未来的安装流程，不执行爬取操作
    # 后续设计文章源插件系统时，可对Spider类增加install&remove方法，分别对应安装和卸载操作，由Django通过命令行负责调用执行
    # install&remove方法描述该插件包的装配信息，用于Django进行相应的安装卸载操作
    def __init__(self, date=None, force='', *a, **kw):
        """
        知乎日报爬虫类，用于爬取&解析知乎日报页面&相关协议
        :param date: 爬取日期，命令行参数，默认为空，即爬取当日最新，内容格式：yyyymmdd
        :param force: 是否强制更新，即待抓取文章已存在于DB，是否强制更新DB&持久化数据，可选值：True/False，默认为False
        """
        super(ZhihuDailySpider, self).__init__(*a, **kw)

        try:
            # 此处由于知乎日报的协议为爬取指定日期的前一天，故需要将Spider接受的date日期+1天作为爬取参数
            if date is not None:
                spider_date = datetime.datetime.strptime(date, '%Y%m%d')
                spider_date += datetime.timedelta(days=1)
                spider_date_str = spider_date.strftime('%Y%m%d')
                self.logger.info('格式化后的知乎爬取日期参数：{}'.format(spider_date_str))
                self.start_urls = ['http://news.at.zhihu.com/api/4/news/before/{}'.format(spider_date_str)]
            else:
                self.start_urls = ['http://news-at.zhihu.com/api/4/news/latest']
        except ValueError:
            self.logger.error('指定的爬取日期错误(yyymmdd)：{}'.format(date))
        self.force = True if force.lower() == 'true' else False
        self.logger.info('指定爬取参数：date={}, force={}'.format(date, self.force))

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

        datetime = time.strptime(content['date'], "%Y%m%d")

        # 设置persistent_path，即爬取数据经过Pipeline持久化时使用的存储路径
        strftime = time.strftime("%Y-%m-%d", datetime)
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

        self.logger.info('处理今日文章，共{:>2}篇'.format(len(content['stories'])))
        for item in content['stories']:
            self.logger.info(item)

            # 从DB中查询该日报文章ID是否已存在，存在则忽略，不存在继续执行后续逻辑
            z = ZhihuItem(daily_id=item['id'], top=item.get('top', False))
            if not self.force and z.exists(spider=self):
                self.logger.warn('该文章已存在于DB，丢弃任务：《{}》'.format(item['title']))
                continue

            # 初步填充ArticleItem数据
            a = ArticleItem()
            a['pub_datetime'] = datetime
            a['source'] = self.source
            a['addition_info'] = z

            # 若对应文章的ZhihuDaily已存在于DB且相应协议中无'top_stories'字段，
            # 则删除item中的addition_info字段，即不更新该存在的记录
            if 'top_stories' not in content and z.exists(spider=self):
                self.logger.warn("附加信息已存在于DB且当前响应中无相关字段，丢弃item['addition_info']")
                del a['addition_info']

            url = 'http://news-at.zhihu.com/api/4/news/{}'.format(z['daily_id'])
            request = scrapy.Request(url, callback=self.parse_article)
            request.meta['item'] = a
            yield request

    def parse_article(self, response):
        content = json.loads(response.body.decode(), encoding='UTF-8')
        a = response.meta['item']

        a['url'] = content.get('share_url', '')
        a['title'] = content.get('title', '')
        if not any([a['title']]):
            self.logger.warn('遇到标题为空的文章 - {}'.format(a['url']))

        # 单独处理type字段为1的情况，即该文章为站外转发文章
        if content.get('type') == 1:
            self.logger.warn('遇到站外文章，单独处理 - {}'.format(a['title']))
            return a

        # 继续填充ArticleItem数据
        a['cover_image'] = content.get('image', content.get('images', [None])[0])
        a['content'] = content.get('body', '')
        self.logger.debug(a)

        # 为图片持久化pipeline执行做数据准备
        a['image_urls'] = [a['cover_image']] if a['cover_image'] is not None else []

        # 格式化content，将其中的img标签src全部导出到image_urls中
        a['image_urls'] += Selector(text=a['content']).css('img::attr(src)').extract()
        self.logger.debug('待处理的图片url(过滤前): {}'.format(a['image_urls']))

        # 过滤掉image_urls中的公式url，目前未找到好方法将其转换为图片持久化
        a['image_urls'] = [img for img in a['image_urls'] if 'equation?tex=' not in img] if any(a['image_urls']) else []
        self.logger.debug('待处理的图片url: {}'.format(a['image_urls']))
        yield a


class ZhihuItem(scrapy.Item):
    daily_id = scrapy.Field()  # 日报文章ID
    top = scrapy.Field()  # 热文标志

    def save_to_db_by_article(self, article, spider):
        zhihu, created = ZhihuDaily.objects.update_or_create(article=article,
                                                             defaults={'daily_id': self.get('daily_id'),
                                                                       'top': self.get('top')})

    def exists(self, spider):
        try:
            zhihu = ZhihuDaily.objects.get(daily_id=self.get('daily_id'))
            spider.logger.debug('测试文章是否存在: {}'.format(self.get('daily_id')))
            return True
        except models.ObjectDoesNotExist:
            return False
