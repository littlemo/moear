import os
import copy
import json
import logging
import hashlib
import stevedore
from collections import OrderedDict

from django.conf import settings
from django.utils import timezone

from celery import shared_task
from posts.models import *
from posts.serializers import *
from spiders.models import *
from spiders.serializers import *

log = logging.getLogger(__name__)


@shared_task
def package_post(post_pk_list, usermeta={}):
    '''
    将传入的 Post 列表打包成 Mobi 文件
    '''
    post_list = [Post.objects.get(pk=pk) for pk in post_pk_list]
    log.debug('Post对象列表: {}'.format(post_list))

    # 将文章列表以时间倒序排列
    post_list.sort(key=lambda post: post.date, reverse=True)

    package_group = OrderedDict()
    for post in post_list:
        # 生成文章数据的字典数据（含元数据）
        postmeta_list = PostMeta.objects.filter(post=post)
        postmeta_data = PostMetaSerializer(postmeta_list, many=True).data
        post_data = PostSerializer(post).data
        post_data['meta'] = postmeta_data

        # 生成爬虫数据的字典数据（含元数据）
        spider_data = SpiderSerializer(post.spider).data
        spdiermeta_list = SpiderMeta.objects.filter(spider=post.spider)
        spidermeta_data = SpiderMetaSerializer(spdiermeta_list, many=True).data
        spider_data['meta'] = spidermeta_data

        # 定义输出字典所用到的键名
        spider_name = post.spider.name
        package_module = spidermeta_data.get('package_module', '')

        # 组装输出字典数据
        package_group.setdefault(package_module, OrderedDict())
        package_group[package_module].setdefault(spider_name, OrderedDict())
        package_group[package_module][spider_name].setdefault(
            'spider', spider_data)
        package_group[package_module][spider_name].setdefault('data', [])
        package_group[package_module][spider_name]['data'].append(post_data)

    log.debug('根据Package&Spider分组并序列化后的数据字典: {}'.format(
        json.dumps(package_group, ensure_ascii=False)))

    for package_module, spider_group in package_group.items():
        for spider_name, package_group in spider_group.items():
            # 定义相关配置数据
            um = copy.deepcopy(usermeta)
            posts_data_raw = package_group.get('data', [])
            um['publish_date'] = posts_data_raw[0].get(
                'date',
                timezone.now().strftime('%Y-%m-%d')).split('T')[0]

            # 通过调用指定 Spider 驱动，对文章列表数据进行格式化
            spider_mgr = stevedore.driver.DriverManager(
                namespace='moear.spider',
                name=spider_name,
                invoke_on_load=True,
            )
            posts_data = spider_mgr.driver.format(posts_data_raw)
            log.debug('经过Spider格式化后的文章列表: {}'.format(
                json.dumps(posts_data, ensure_ascii=False)))

            # 通过调用指定 Package 驱动，获取最终打包返回的mobi文件数据
            spider_dict = package_group.get('spider', {})
            package_mgr = stevedore.driver.DriverManager(
                namespace='moear.package',
                name=package_module,
                invoke_on_load=True,
                invoke_args=(spider_dict,),
                invoke_kwds={'usermeta': um},
            )
            book_file, book_ext = package_mgr.driver.generate(posts_data)

            # 从系统settings中获取mobi暂存路径，并将book_file保存成文件
            book_filename = \
                '{spider_display_name}[{publish_date}]_{md5}.{ext}'.format(
                    spider_display_name=spider_dict.get('display_name'),
                    publish_date=um.get('publish_date'),
                    md5=_md5_posts_list(posts_data_raw),
                    ext=book_ext,
                )
            book_abspath = os.path.join(
                settings.BOOK_PACKAGE_ROOT, book_filename)
            with open(book_abspath, 'wb') as fh:
                fh.write(book_file)


def _md5_posts_list(posts):
    origin_url_list = [post.get('origin_url', '') for post in posts]
    log.debug('origin_url_list: {}'.format(origin_url_list))
    origin_url_str = ''.join(origin_url_list)
    return hashlib.md5(origin_url_str.encode('utf-8')).hexdigest()[:16].upper()
