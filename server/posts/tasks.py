import logging
import json

import stevedore
from django.utils import timezone
from celery import shared_task

from .serializers import *
from spiders.models import Spider


log = logging.getLogger(__name__)


@shared_task
def spider_post(spider_pk):
    """
    爬取文章数据
    """
    spider = Spider.objects.get(pk=spider_pk)
    mgr = stevedore.NamedExtensionManager(
        namespace='moear.spider',
        names=[spider.name],
        invoke_on_load=True,
        invoke_args=(),
    )

    def crawl(ext, *args):
        rc = ext.obj.crawl()
        log.info('[{name}]爬取返回包：{pack}'.format(
            name=ext.name, pack=rc))
        data = json.loads(rc, encoding='UTF-8')
        return (ext.name, data)

    results = mgr.map(crawl)
    log.debug('结果对象：{results}'.format(
        results=results))

    results.reverse()
    for name, data in results:
        log.info('[{name}]处理爬虫返回数据，并持久化'.format(name=name))
        for d in data:
            post_serializer = PostSerializer(data=d)
            if not post_serializer.is_valid():
                log.error(post_serializer.errors)
                break
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
                break
            postmeta_serializer.save(post=post_serializer.instance)
