from django.db import models
from django.utils.translation import gettext_lazy as _


class Spider(models.Model):
    """
    爬虫信息数据模型

    用来指示爬虫的作者、名称、描述等常规信息
    """
    name = models.CharField(
        verbose_name=_('名称'),
        max_length=255,
        unique=True)  # 此处为spider对应的name，唯一
    display_name = models.CharField(
        verbose_name=_('显示名称'),
        unique=True,
        max_length=255)  # 用于界面显示
    author = models.CharField(
        verbose_name=_('作者'),
        max_length=255)
    email = models.EmailField(
        verbose_name=_('邮箱'))
    description = models.TextField(
        verbose_name=_('描述'),
        blank=True,
        default='')  # 描述信息

    enabled = models.BooleanField(
        verbose_name=_('开启'),
        default=True)

    def __str__(self):
        output = '[{name}]({author}){display_name}'.format(
            name=self.name,
            author=self.author,
            display_name=self.display_name)
        return output

    class Meta:
        verbose_name = _('爬虫信息')
        verbose_name_plural = verbose_name
