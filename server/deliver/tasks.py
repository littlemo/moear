import logging

from celery import task
from django.conf import settings
# from django.utils import timezone
from django.core.mail import EmailMessage
from django.utils.translation import gettext_lazy as _

log = logging.getLogger(__name__)


@task(time_limit=settings.EMAIL_TIME_LIMIT)
def deliver_book_task(from_email, email_list, filename, attachments):
    assert isinstance(email_list, list) or isinstance(email_list, tuple)

    subject = 'MoEar · {filename}'.format(filename=filename.split('_')[0])
    msg = EmailMessage(
        subject,
        _('由 MoEar 为您投递'),
        from_email,
        email_list)
    msg.attach(attachments)
    msg.send()
    log.info(_('投递书籍【{filename}】到: {email_list}').format(
        filename=filename,
        email_list=', '.join(email_list)))
