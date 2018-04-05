import os
import copy
import json
import logging
import stevedore

from celery import shared_task
from django.conf import settings
from django.utils import timezone

from .utils import trans_to_package_group, posts_list_md5, yield_sec_level_dict
from core.models import UserMeta
from deliver.models import DeliverLog
from spiders.models import Spider
from deliver.tasks import deliver_book_task

log = logging.getLogger(__name__)


@shared_task
def package_post(post_pk_list, usermeta={}, dispatch=True):
    '''
    将传入的 Post 列表打包成 Mobi 文件，并进行投递

    :param post_pk_list: 文章主键列表
    :type post_pk_list: list(int)
    :param dict usermeta: 关键字参数，可选，用于提供定制的配置项，以覆盖插件中的默认配置
    :param bool dispatch: 关键字参数，可选，
        用于指定是否在打包后立刻执行投递逻辑，默认为True
    '''
    log.info('待打包文章列表({num}): {post_pk_list}'.format(
        num=len(post_pk_list),
        post_pk_list=post_pk_list))
    package_group = trans_to_package_group(post_pk_list)
    for package_module, spider_name, book_group \
            in yield_sec_level_dict(package_group):
        # 定义相关配置数据
        um = copy.deepcopy(usermeta)
        posts_data_raw = book_group.get('data', [])
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

        # 创建投递日志
        deliver_log = DeliverLog(
            spider=Spider.objects.get(name=spider_name),
            status=DeliverLog.PACKAGING,
        )
        deliver_log.save()

        # 通过调用指定 Package 驱动，获取最终打包返回的mobi文件数据
        spider_dict = book_group.get('spider', {})
        # 此处为便于在Amazon后台以及设备中识别期刊日期，故作为Trick使用
        # 因为，在新版Kindle系统中会在书籍下方显示作者信息，而非旧版时的日期信息，
        # 对于每日更新的期刊很容易混淆，故在作者信息后追加期刊发布日期
        spider_dict['author'] = '{author}[{pub_date}]'.format(
            author=spider_dict['author'],
            pub_date=um['publish_date'])
        package_mgr = stevedore.driver.DriverManager(
            namespace='moear.package',
            name=package_module,
            invoke_on_load=True,
            invoke_args=(spider_dict,),
            invoke_kwds={'usermeta': um},
        )
        try:
            book_ext = package_mgr.driver.ext
            book_file = package_mgr.driver.generate(posts_data)
        except Exception as e:
            deliver_log.status = DeliverLog.FAILED
            deliver_log.save()
            raise e

        # 从系统settings中获取mobi暂存路径，并将book_file保存成文件
        book_filename = \
            '{spider_display_name}[{publish_date}]_{md5}.{ext}'.format(
                spider_display_name=spider_dict.get('display_name'),
                publish_date=um.get('publish_date'),
                md5=posts_list_md5(posts_data_raw),
                ext=book_ext,
            )
        book_abspath = os.path.join(
            settings.BOOK_PACKAGE_ROOT, book_filename)
        # TODO 增加对文件的zip压缩支持，从而减小投递流量消耗
        with open(book_abspath, 'wb') as fh:
            fh.write(book_file)
        deliver_log.file_name = book_filename
        deliver_log.file_size = os.path.getsize(book_abspath)
        deliver_log.status = DeliverLog.PACKAGED
        deliver_log.save()

        # 将生成的书籍文件分发到订阅的设备地址上
        if not dispatch:
            return

        feed_usermeta = UserMeta.objects.filter(
            name='moear.spider.feeds',
            value__contains=spider_name)

        email_addr_list = []
        user_list = []
        for usermeta in feed_usermeta:
            user_list.append(usermeta.user)
            feed_address_usermeta = UserMeta.objects.get(
                user=usermeta.user,
                name='moear.device.addr')
            if feed_address_usermeta.value:
                email_addr_list.append(feed_address_usermeta.value)

        log.info('订阅了【{spider_name}】的用户设备地址: {addr_list}'.format(
            spider_name=spider_name,
            addr_list=email_addr_list))

        deliver_log.users.set(user_list)
        deliver_log.status = DeliverLog.DELIVERING
        deliver_log.save()

        if len(email_addr_list) == 0:
            deliver_log.status = DeliverLog.FAILED
            deliver_log.save()
            return
        # HINT 此处为了节省流量，进行了合并投递，但传说一份邮件超过15个不同
        # 的【发送至Kindle】电子邮箱，会被认定为垃圾邮件而被Amazon拒绝接收，
        # 但我没有验证条件，故当前仅留下说明信息

        # HINT 同样传说附加大于50MB会投递失败，待验证
        try:
            deliver_book_task.delay(
                email_addr_list,
                book_filename.split('_')[0],
                book_abspath,
                deliver_log_pk=deliver_log.pk)
        except Exception as e:
            deliver_log.status = DeliverLog.FAILED
            deliver_log.save()
            raise e
