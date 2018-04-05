from django.test import TestCase

import logging

from .serializers import *


log = logging.getLogger(__name__)


class SpiderSerializerTests(TestCase):
    def setUp(self):
        self.fake_data_spider = {
            'name': 'zhihu_daily',
            'display_name': '知乎日报',
            'author': '小貘',
            'email': 'moore@moorehy.com',
            'description':
                '每天三次，每次七分钟。在中国，资讯类移动应用的人均阅读时长是 '
                '5 分钟，而在知乎日报，这个数字是 21',
            'meta': {
                'img_cover': 'img_cover_path',
                'image_filter': ['equation\\?tex='],
                'book_mode': 'periodical',
                'language': 'zh-CN',
                'img_masthead': 'img_masthead_path',
                'css_package': 'css_package_path',
                'package_module': 'mobi',
            }
        }

    def test_create(self):
        '''
        根据砖数据进行Spider模型的序列化创建
        '''
        spider_serializer = SpiderSerializer(
            data=self.fake_data_spider, exclude=['enabled'])
        if not spider_serializer.is_valid():
            log.error(spider_serializer.errors)
        self.assertTrue(spider_serializer.is_valid())

        spider_serializer.save()
        log.debug(spider_serializer.instance)

        self.assertEqual(
            Spider.objects.get(name=self.fake_data_spider.get('name')),
            spider_serializer.instance)

    def test_update(self):
        '''
        测试更新 Spider 数据
        '''
        # 创建原始条目
        self.test_create()

        # 修改数据
        self.fake_data_spider['description'] = 'Or2'

        # 执行条目更新
        self.test_create()


class SpiderMetaSerializerTests(TestCase):
    def setUp(self):
        self.fake_data_spider = {
            'name': 'zhihu_daily',
            'display_name': '知乎日报',
            'author': '小貘',
            'email': 'moore@moorehy.com',
            'description':
                '每天三次，每次七分钟。在中国，资讯类移动应用的人均阅读时长是 '
                '5 分钟，而在知乎日报，这个数字是 21',
            'meta': {
                'img_cover': 'img_cover_path',
                'image_filter': '["zhihu.com/equation"]',
                'book_mode': 'periodical',
                'language': 'zh-CN',
                'img_masthead': 'img_masthead_path',
                'css_package': 'css_package_path',
                'package_module': 'mobi',
            }
        }
        spider_serializer = SpiderSerializer(
            data=self.fake_data_spider, exclude=['enabled'])
        if not spider_serializer.is_valid():
            log.error(spider_serializer.errors)
        spider_serializer.save()

        self.spider = spider_serializer.instance

    def test_create(self):
        '''
        测试通过序列化器创建指定 Spider 的元数据对象
        '''
        spidermeta_serializer = SpiderMetaSerializer(
            data=self.fake_data_spider.get('meta'), many=True)
        if not spidermeta_serializer.is_valid():
            log.error(spidermeta_serializer.errors)
        self.assertTrue(spidermeta_serializer.is_valid())

        spidermeta_serializer.save(spider=self.spider)
        log.debug(spidermeta_serializer.instance)
        log.debug(spidermeta_serializer.data)
        self.assertEqual(
            self.fake_data_spider.get('meta'),
            spidermeta_serializer.data)

    def test_update(self):
        '''
        测试更新 Spider 元数据
        '''
        # 创建原始条目
        self.test_create()

        # 修改元数据
        self.fake_data_spider['meta']['css_package'] = 'css/package/path'

        # 执行条目更新
        self.test_create()
