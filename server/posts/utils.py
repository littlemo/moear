import json
import logging
import hashlib
from collections import OrderedDict

from posts.models import Post, PostMeta
from posts.serializers import PostSerializer, PostMetaSerializer
from spiders.models import SpiderMeta
from spiders.serializers import SpiderSerializer, SpiderMetaSerializer


log = logging.getLogger(__name__)


def trans_to_package_group(post_pk_list):
    '''
    将传入的文章主键列表转换成可用于分组打包的字典数据

    :param list post_pk_list: 文章主键列表
    :return: 根据打包模块、爬虫分类的字典数据
    :rtype: dict
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

    return package_group
