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

    package_group = defaultdict(list)
    for post in post_list:
        postmeta_list = PostMeta.objects.filter(post=post)
        postmeta_data = PostMetaSerializer(postmeta_list, many=True).data
        post_data = PostSerializer(post).data
        post_data['meta'] = postmeta_data
        package_group[post.spider.name].append(post_data)

    log.debug('根据Spider分组并序列化后的文章列表: {}'.format(package_group))
