import logging
import random

from celery import task, shared_task
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.utils.translation import gettext_lazy as _

from spiders.models import Spider, SpiderMeta
from spiders.tasks import spider_post
from posts.tasks import package_post
from .models import UserMeta

log = logging.getLogger(__name__)


@task(time_limit=settings.EMAIL_TIME_LIMIT)
def account_send_email_task(subject, bodies, from_email, email):
    if 'txt' in bodies:
        msg = EmailMultiAlternatives(
            subject,
            bodies['txt'],
            from_email,
            [email])
        if 'html' in bodies:
            msg.attach_alternative(bodies['html'], 'text/html')
    else:
        msg = EmailMessage(
            subject,
            bodies['html'],
            from_email,
            [email])
        msg.content_subtype = 'html'  # Main content is now text/html
    msg.send()
    log.info(_('发送账户邮件到: %s'), email)


@shared_task
def periodic_chain_crawl_package_deliver(spider_name):
    '''
    周期链式调用爬取、打包、投递

    :param str spider_name: 当前任务处理的Spider名称
    '''
    spider = Spider.objects.get(name=spider_name)
    crawl_random_delay = SpiderMeta.objects.get(
        spider=spider, name='crawl_random_delay').value
    delay = random.randint(0, int(crawl_random_delay))
    log.info('随机延迟【{delay}】秒爬取【{name}】源'.format(
        delay=delay,
        name=spider.display_name))

    # 获取订阅设备地址列表
    feed_usermeta = UserMeta.objects.filter(
        name='moear.spider.feeds',
        value__contains=spider_name)
    email_addr_list = []
    for usermeta in feed_usermeta:
        feed_address_usermeta = UserMeta.objects.get(
            user=usermeta.user,
            name='moear.device.addr')
        if feed_address_usermeta.value:
            email_addr_list.append(feed_address_usermeta.value)

    # 根据订阅数量决定执行的任务内容
    if len(email_addr_list) == 0:
        # 仅执行爬取任务
        log.info('该文章源【{display_name}】无订阅的设备地址，故仅执行爬取任务'.format(
            display_name=spider.display_name))
        c = spider_post.s(spider_name).set(countdown=delay)
    else:
        # 任务链，依次执行爬取、打包、投递，目前其中打包和投递实现在package_post任务中
        c = spider_post.s(spider_name).set(countdown=delay) | package_post.s()
    c.delay()
