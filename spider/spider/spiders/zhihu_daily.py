# -*- coding: utf-8 -*-
import json

import scrapy


class ZhihuDailySpider(scrapy.Spider):
    name = "zhihu_daily"
    allowed_domains = ["zhihu.com"]
    start_urls = (
        'http://news-at.zhihu.com/api/4/news/latest',
    )

    def parse(self, response):
        return self.yield_article_request(response=response)

    def yield_article_request(self, response):
        content_raw = response.body.decode()
        self.logger.debug('响应body原始数据：{}'.format(content_raw))
        content = json.loads(content_raw, encoding='UTF-8')
        self.logger.debug(content)

        self.logger.info('日期：{}'.format(content['date']))

        self.logger.info('今日文章')
        for item in content['stories']:
            self.logger.info(item)

        self.logger.info('头条文章')
        for item in content['top_stories']:
            self.logger.info(item)
