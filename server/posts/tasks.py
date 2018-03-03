import logging
import json

from django.utils import timezone
from celery import shared_task
from moear_spider_zhihudaily import entry

from .serializers import *


log = logging.getLogger(__name__)


@shared_task
def spider_post(spider_pk):
    """
    爬取文章数据
    """
    zhihu = entry.ZhihuDaily()
    rc = zhihu.crawl()
    log.info('爬取返回包：{}'.format(rc))
    data = json.loads(rc, encoding='UTF-8')

    for d in data:
        post_serializer = PostSerializer(data=d)
        if not post_serializer.is_valid():
            log.error(post_serializer.errors)
            return
        date = timezone.datetime.strptime(
            d.get('date', ''), '%Y-%m-%d %H:%M:%S')
        date = timezone.make_aware(date, timezone.get_current_timezone())
        # TODO Fix 如果强制设置date(文章创建时间)
        post_serializer.save()

        metadata = d.pop('meta', [])
        postmeta_serializer = PostMetaSerializer(
            data=metadata, many=True)
        if not postmeta_serializer.is_valid():
            log.error(postmeta_serializer.errors)
            return
        postmeta_serializer.save(post=post_serializer.instance)
