import logging
from collections import defaultdict

from celery import shared_task
from posts.models import *
from posts.serializers import *
from spiders.models import *
from spiders.serializers import *

log = logging.getLogger(__name__)


@shared_task
def package_post(post_pk_list):
    '''
    将传入的 Post 列表打包成 Mobi 文件
    '''
    post_list = [Post.objects.get(pk=pk) for pk in post_pk_list]

    # 将文章列表以时间倒序排列
    post_list.sort(key=lambda post: post.date, reverse=True)

    package_group = defaultdict(dict)
    for post in post_list:
        postmeta_list = PostMeta.objects.filter(post=post)
        postmeta_data = PostMetaSerializer(postmeta_list, many=True).data
        post_data = PostSerializer(post).data
        post_data['meta'] = postmeta_data

        spider_name = post.spider.name

        spider_data = SpiderSerializer(post.spider).data
        spdiermeta_list = SpiderMeta.objects.filter(spider=post.spider)
        spidermeta_data = SpiderMetaSerializer(spdiermeta_list, many=True).data
        spider_data['meta'] = spidermeta_data

        package_module = spidermeta_data.get('package_module', '')

        package_group[package_module].setdefault(spider_name, {})
        log.debug(package_group)
        package_group[package_module][spider_name].setdefault(
            'spider', spider_data)
        log.debug(package_group)
        package_group[package_module][spider_name].setdefault('data', [])
        package_group[package_module][spider_name]['data'].append(post_data)
