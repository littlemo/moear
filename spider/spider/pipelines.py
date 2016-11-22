# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import os

from bs4 import BeautifulSoup
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes


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
        info.spider.logger.info('保存图片：{} | {} | {}'.format(response, request, url))
        return url


class PagePersistentPipeline(object):
    """
    将爬取到的文章内容持久化到指定路径
    使用spider中提供的persistent_path作为子路径，如：zhihu_daily/yyyy-mm-dd/xxxx.html
    """

    def process_item(self, item, spider):
        # 将item['content']中的全部img替换为本地化后的url，此处需使用BS库
        soup = BeautifulSoup(item['content'], "lxml")
        img_list = soup.find_all('img')
        for i in img_list:
            img_src = i.get('src')
            for result in item['images']:
                if img_src == result['url']:
                    raw_path_list = result['path'].split('/')
                    i['src'] = os.path.join(raw_path_list[-2], raw_path_list[-1])
                    spider.logger.info('文章({})的正文img保存成功: {}'.format(item['title'], img_src))
                    break
        item['content'] = soup.div.prettify(encoding='utf8')

        # 填充cover_image_local路径值
        for result in item['images']:
            if item['cover_image'] == result['url']:
                item['cover_image_local'] = result['path']
                break

        # 将item['content']保存到本地，路径使用(<ARTICLE_PAGE_STORE_BASE>/spider.name/yyyy-mm-dd/xxxx.html)
        page_store_path = spider.settings.get('PAGE_STORE', '.')
        article_html_name = hashlib.sha1(to_bytes(item['url'])).hexdigest()
        html_name = '{}.html'.format(article_html_name)
        item['url_local'] = os.path.join(spider.persistent_path, html_name)
        page_store = os.path.join(page_store_path, item['url_local'])

        # 创建目标dirname
        dirname = os.path.dirname(page_store)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # 将文章正文本地化
        with open(page_store, 'wb') as f:
            f.write(item['content'])

        # 清空content值，为优化log打印信息
        item['content'] = None
        return item


class ItemPersistentPipeline(object):
    """
    将item相关字段及附加信息保存到DB
    """

    def process_item(self, item, spider):
        item.save_to_db(spider=spider)
        spider.logger.info('保存item到DB: \n%s' % item)
        return item
