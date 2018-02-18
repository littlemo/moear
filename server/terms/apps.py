from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TermsConfig(AppConfig):
    name = 'terms'
    verbose_name = _('分类组件')
