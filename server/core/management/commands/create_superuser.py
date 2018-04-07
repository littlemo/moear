import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = '创建超级管理员账户，若已存在则更新管理员账户密码'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username', nargs='?', type=str,
            default=settings.ADMIN_USERNAME,
            help=_('用户名，默认为 $ADMIN_USERNAME'))
        parser.add_argument(
            '--email', nargs='?', type=str,
            default=settings.ADMIN_EMAIL,
            help=_('邮箱地址，默认为 $ADMIN_EMAIL'))
        parser.add_argument(
            '--password', nargs='?', type=str,
            default=settings.ADMIN_PASSWORD,
            help=_('密码，默认为 $ADMIN_PASSWORD'))

    def handle(self, *args, **options):
        email = options.get('email')
        username = options.get('username')
        password = options.get('password')
        log.debug('用户参数：{username} {email} {password}'.format(
            username=username,
            email=email,
            password=password))
        try:
            admin = User.objects.get(username=username)
        except User.DoesNotExist:
            User.objects.create_superuser(username, email, password)
            return
        log.info('待创建用户已存在，仅执行修改密码操作！')
        admin.set_password(password)
