import json
import logging

import stevedore
from django.utils import timezone
from celery import shared_task

from posts.serializers import *
from spiders.models import Spider


log = logging.getLogger(__name__)


@shared_task
def spider_post(spider_name):
    """
    爬取文章数据
    """
    spider = Spider.objects.get(name=spider_name)
    mgr = stevedore.NamedExtensionManager(
        namespace='moear.spider',
        names=[spider.name],
        invoke_on_load=True,
    )

    def crawl(ext, *args):
        rc = ext.obj.crawl()
        data = json.dumps(rc, ensure_ascii=False)
        log.debug('[{name}]爬取返回包：{pack}'.format(
            name=ext.name, pack=data))
        return (ext.name, rc)

    results = mgr.map(crawl)
    log.debug('结果对象：{results}'.format(
        results=results))

    post_pk_list = []
    for name, data in results:
        log.info('[{name}]处理爬虫返回数据，并持久化'.format(name=name))
        data.reverse()
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
            post_pk_list.append(post_serializer.instance.pk)

            metadata = d.pop('meta', [])
            postmeta_serializer = PostMetaSerializer(
                data=metadata, many=True)
            if not postmeta_serializer.is_valid():
                log.error(postmeta_serializer.errors)
                break
            postmeta_serializer.save(post=post_serializer.instance)
    log.info('完成文章爬取({num}): {post_pk_list}'.format(
        num=len(post_pk_list),
        post_pk_list=post_pk_list))
    return post_pk_list
