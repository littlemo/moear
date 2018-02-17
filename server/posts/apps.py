from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PostsConfig(AppConfig):
    name = 'posts'
    verbose_name = _('文章组件')
