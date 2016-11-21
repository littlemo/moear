# -*- coding: utf-8 -*-
import scrapy


class ZhihuDailySpider(scrapy.Spider):
    name = "zhihu_daily"
    allowed_domains = ["zhihu.com"]
    start_urls = (
        'http://www.zhihu.com/',
    )

    def parse(self, response):
        pass
