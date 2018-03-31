from django.db import models
from django.utils.translation import gettext_lazy as _


class DeliverLog(models.Model):
    '''
    投递日志
    '''
    STATUS_CHOICES = (
        ('packaged', _('已打包')),
        ('delivering', _('投递中')),
        ('completed', _('完成')),
        ('failed', _('失败')),
    )

    id = models.BigAutoField(
        primary_key=True)
    user = models.ManyToManyField(
        'auth.User',
        verbose_name=_('投递用户'))
    spider = models.ForeignKey(
        'spiders.Spider',
        verbose_name=_('爬虫信息'),
        db_index=True,
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_NULL)
    file_name = models.CharField(
        verbose_name=_('附件名称'),
        max_length=255)
    file_size = models.BigIntegerField(
        verbose_name=_('附件大小'),
        default=0)
    status = models.CharField(
        verbose_name=_('投递状态'),
        default='failed',
        choices=STATUS_CHOICES,
        max_length=20)
    date = models.DateTimeField(
        verbose_name=_('投递时间'),
        auto_now_add=True)

    class Meta:
        verbose_name = _('投递日志')
        verbose_name_plural = verbose_name
