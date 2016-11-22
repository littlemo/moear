# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    pub_datetime = scrapy.Field()  # 文章发布的日期时间，需使用time包格式化为struct_time对象
    title = scrapy.Field()  # 文章标题
    source = scrapy.Field()  # 文章来源，使用Django的Source模型填充
    url = scrapy.Field()  # 文章URL
    content = scrapy.Field()  # 文章正文

    addition_info = scrapy.Field()  # 一些具体文章源的附加信息，如知乎日报的封面图、是否热文、文章ID

    # 以下参数为pipelines处理时使用
    local_url = scrapy.Field()  # 文章持久化后的本地路径
    image_urls = scrapy.Field()  # 图片链接
    images = scrapy.Field()  # 图片存储返回
