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

        # 通过调用指定 Package 驱动，获取最终打包返回的mobi文件数据
        spider_dict = book_group.get('spider', {})
        package_mgr = stevedore.driver.DriverManager(
            namespace='moear.package',
            name=package_module,
            invoke_on_load=True,
            invoke_args=(spider_dict,),
            invoke_kwds={'usermeta': um},
        )
        book_ext = package_mgr.driver.ext
        book_file = package_mgr.driver.generate(posts_data)

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
        with open(book_abspath, 'wb') as fh:
            fh.write(book_file)

        # 将生成的书籍文件分发到订阅的设备地址上
        if not dispatch:
            return

        feed_usermeta = UserMeta.objects.filter(
            name='moear.spider.feeds',
            value__contains=spider_name)

        email_addr_list = []
        for usermeta in feed_usermeta:
            feed_address_usermeta = UserMeta.objects.get(
                user=usermeta.user,
                name='moear.device.addr')
            email_addr_list.append(feed_address_usermeta.value)

        log.info('订阅了【{spider_name}】的用户设备地址: {addr_list}'.format(
            spider_name=spider_name,
            addr_list=email_addr_list))

        deliver_book_task.delay(
            email_addr_list,
            book_filename.split('_')[0],
            book_abspath)
