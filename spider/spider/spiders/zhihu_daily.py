# -*- coding: utf-8 -*-
import json
import time

import scrapy


class ZhihuDailySpider(scrapy.Spider):
    # 来源名称，唯一，长度<50，用于文章源模型索引创建后不可修改
    name = "zhihu_daily"

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
    def parse(self, response):
        return self.yield_article_request(response=response)

    def yield_article_request(self, response):
        content_raw = response.body.decode()
        self.logger.debug('响应body原始数据：{}'.format(content_raw))
        content = json.loads(content_raw, encoding='UTF-8')
        self.logger.debug(content)


        self.logger.info('今日文章')
        for item in content['stories']:
            self.logger.info(item)
        self.datetime = time.strptime(content['date'], "%Y%m%d")
        self.logger.info('日期：{}'.format(self.datetime))

        self.logger.info('头条文章')
        for item in content['top_stories']:
            self.logger.info(item)


class ZhihuItem(scrapy.Item):
    daily_id = scrapy.Field()  # 日报文章ID
    cover_images = scrapy.Field()  # 文章封面图片
    top = scrapy.Field()  # 热文标志
