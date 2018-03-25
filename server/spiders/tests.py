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
        spider_serializer = SpiderSerializer(data=self.fake_data_spider)
        if not spider_serializer.is_valid():
            log.error(spider_serializer.errors)
        self.assertTrue(spider_serializer.is_valid())

        spider_serializer.save()

        self.assertEqual(
            Spider.objects.get(name=self.fake_data_spider.get('name')),
            spider_serializer.instance)
