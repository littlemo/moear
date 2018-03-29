from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DeliverConfig(AppConfig):
    name = 'deliver'
    verbose_name = _('投递组件')
