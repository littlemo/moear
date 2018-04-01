import os
import logging

from celery import task
from django.conf import settings
from email import encoders
from email.mime.base import MIMEBase
from django.core.mail import EmailMessage
from django.utils.translation import gettext_lazy as _

from deliver.models import DeliverLog

log = logging.getLogger(__name__)


@task(time_limit=settings.EMAIL_TIME_LIMIT)
def deliver_book_task(
        recipient,
        subject,
        book_abspath,
        from_email=settings.DEFAULT_FROM_EMAIL,
        deliver_log_pk=None):
    '''
    投递书籍任务

    将传入的书籍作为附件发送给接收邮箱列表中

    :param recipient: 接收人邮箱地址
    :type recipient: list or tuple
    :param str subject: 邮件主题，将被强制添加 ``MoEar · `` 前缀
    :param str book_abspath: 作为附件书籍的绝对路径
    :param str from_email: 发件人邮箱地址，默认使用 ``settings.DEFAULT_FROM_EMAIL``
    '''
    assert isinstance(recipient, list) or isinstance(recipient, tuple)
    assert isinstance(book_abspath, str)

    # 读取书籍文件
    with open(book_abspath, 'rb') as fh:
        book_file = fh.read()

    # 构建书籍附件对象
    att = MIMEBase('application', 'octet-stream')
    att.set_payload(book_file)
    att.add_header(
        'Content-Disposition', 'attachment',
        filename=('gbk', '', os.path.basename(book_abspath)))
    encoders.encode_base64(att)

    # 构建邮件消息对象
    subject_prefix = 'MoEar · '
    full_subject = '{prefix}{subject}'.format(
        prefix=subject_prefix,
        subject=subject)
    recipient = [i for i in recipient if i]  # 去掉空值
    msg = EmailMessage(
        full_subject,
        _('由 MoEar 为您投递'),
        from_email,
        recipient)
    msg.attach(att)

    if deliver_log_pk:
        deliver_log = DeliverLog.objects.get(pk=deliver_log_pk)
        deliver_log.status = DeliverLog.COMPLETED
        deliver_log.save()

    # 发送邮件
    try:
        msg.send()
    except Exception as e:
        if deliver_log_pk:
            deliver_log.status = DeliverLog.FAILED
            deliver_log.save()
        raise e

    log.info(_('投递书籍【{subject}】到: {recipient}').format(
        subject=subject,
        recipient=', '.join(recipient)))
