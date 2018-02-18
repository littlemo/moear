from django.db import models
from django.utils.translation import ugettext_lazy as _


class Option(models.Model):
    """
    站点配置

    网站的设置和选项，用于设置站点信息、插件相关等额外配置
    """
    AUTOLOAD_CHOICES = (
        ('yes', _('是')),
        ('no', _('否')),
    )

    id = models.BigAutoField(
        primary_key=True)
    key = models.CharField(
        verbose_name=_('键名'),
        db_index=True,
        unique=True,
        max_length=255)
    value = models.TextField(
        verbose_name=_('键值'))
    autoload = models.CharField(
        verbose_name=_('自动载入'),
        blank=True,
        default='yes',
        choices=AUTOLOAD_CHOICES,
        max_length=20)

    def __str__(self):
        return '[{id}]{key} => {value}'.format(
            id=self.id,
            key=self.key,
            value=self.value)

    class Meta:
        verbose_name = _('站点配置')
        verbose_name_plural = verbose_name


class UserMeta(models.Model):
    """
    用户元数据模型

    用于存储指定用户的元数据信息，便于对该用户进行参数定制修改，可与插件/爬虫配合使用
    """
    id = models.BigAutoField(
        primary_key=True)
    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('用户信息'),
        db_index=True,
        on_delete=models.CASCADE)
    key = models.CharField(
        verbose_name=_('键名'),
        db_index=True,
        blank=True,
        null=True,
        default=None,
        max_length=255)
    value = models.TextField(
        verbose_name=_('键值'),
        blank=True,
        null=True,
        default=None)

    def __str__(self):
        output = '[{id}]{key} => {value}'.format(
            id=self.id,
            key=self.key,
            value=self.value)
        return output

    class Meta:
        verbose_name = _('用户元数据')
        verbose_name_plural = verbose_name
