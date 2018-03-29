import logging

from celery import task
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.utils.translation import gettext_lazy as _

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
