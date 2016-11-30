# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import time

import scrapy
from django.utils import timezone

from articles.models import Article
from articles.models import Source


class ArticleItem(scrapy.Item):
    pub_datetime = scrapy.Field()  # 文章发布的日期时间，需使用time包格式化为struct_time对象
    title = scrapy.Field()  # 文章标题
    source = scrapy.Field()  # 文章来源，使用Django的Source模型填充
    url = scrapy.Field()  # 文章URL
    cover_image = scrapy.Field()  # 文章封面图片
    content = scrapy.Field()  # 文章正文

    addition_info = scrapy.Field()  # 一些具体文章源的附加信息，如知乎日报的是否热文、文章ID

    # 以下参数为pipelines处理时使用
    url_local = scrapy.Field()  # 文章持久化后的本地路径
    cover_image_local = scrapy.Field()  # 文章封面图片持久化后的本地路径

    image_urls = scrapy.Field()  # 图片链接
    images = scrapy.Field()  # 图片存储返回

    def save_to_db(self, spider):
        pub_datetime = timezone.datetime.fromtimestamp(time.mktime(self.get('pub_datetime')),
                                                       tz=timezone.get_current_timezone())
        article, created = Article.objects.update_or_create(url=self.get('url'),
                                                            defaults={'pub_datetime': pub_datetime,
                                                                      'title': self.get('title'),
                                                                      'source': self.get('source'),
                                                                      'url_local': self.get('url_local'),
                                                                      'cover_image': self.get('cover_image'),
                                                                      'cover_image_local': self.get(
                                                                          'cover_image_local')})

        try:
            if any([self.get('addition_info')]):
                self.get('addition_info').save_to_db_by_article(article, spider)
        except Exception as e:
            spider.logger.error('调用附加信息save_to_db_by_article方法失败：{}'.format(e))


class SourceItem(scrapy.Item):
    """
    此模型默认使用spider信息填充，可手动修改
    """
    name = scrapy.Field()  # 来源名称，唯一，长度<50
    author = scrapy.Field()  # 组件作者，长度<50
    verbose_name = scrapy.Field()  # 显示名称，长度<100
    description = scrapy.Field()  # 描述信息，长度<255

    def save_to_db(self):
        src, created = Source.objects.update_or_create(name=self.get('name'),
                                                       defaults={'author': self.get('author', None),
                                                                 'verbose_name': self.get('verbose_name'),
                                                                 'description': self.get('description', None)})
        return src
