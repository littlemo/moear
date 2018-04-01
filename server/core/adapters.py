import logging

from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.signals import user_signed_up

from .tasks import account_send_email_task
from .models import Option

log = logging.getLogger(__name__)


class AccountAdapter(DefaultAccountAdapter):
    '''
    定制的 AllAuth 账户适配器，主要用于支持异步邮件发送
    '''
    def send_mail(self, template_prefix, email, context):
        subject = render_to_string('{0}_subject.txt'.format(template_prefix),
                                   context)
        # remove superfluous line breaks
        subject = " ".join(subject.splitlines()).strip()
        subject = self.format_email_subject(subject)

        from_email = self.get_from_email()

        bodies = {}
        for ext in ['html', 'txt']:
            try:
                template_name = '{0}_message.{1}'.format(template_prefix, ext)
                bodies[ext] = render_to_string(template_name,
                                               context).strip()
            except TemplateDoesNotExist:
                if ext == 'txt' and not bodies:
                    # We need at least one body
                    raise

        account_send_email_task.delay(subject, bodies, from_email, email)

    def is_open_for_signup(self, request):
        if hasattr(request, 'session') and request.session.get(
                'account_verified_email'):
            return True
        return Option().open_for_signup

    def get_user_signed_up_signal(self):
        return user_signed_up
