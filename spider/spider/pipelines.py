# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class ValidationPipeline(object):
    """
    验证item是否合法，url&title&pub_datetime&content皆不可为空
    """
    def process_item(self, item, spider):
        if not any([item['url']]):
            raise DropItem('丢弃url为空的item: {}'.format(item))
        if not any([item['title']]):
            raise DropItem('丢弃标题为空的item: {}'.format(item))
        if not any([item['pub_datetime']]):
            raise DropItem('丢弃发布时间为空的item: {}'.format(item))
        if not any([item['content']]):
            raise DropItem('丢弃内容为空的item: {}'.format(item))
        return item


class MoEarImagesPipeline(ImagesPipeline):
    """
    定制ImagesPipeline，实现图片保存路径的自定义
    """
    def file_path(self, request, response=None, info=None):
        url = super(MoEarImagesPipeline, self).file_path(request, response=response, info=info)
        url = os.path.join(info.spider.persistent_path, 'img', url.split('/')[-1])
        info.spider.logger.info('保存图片：{}|{}|{}'.format(response, request, url))
        return url
