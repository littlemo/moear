from django.db import models
from django.utils.translation import gettext_lazy as _


class DeliverLog(models.Model):
    '''
    投递日志
    '''
    PACKAGING = 'packaging'
    PACKAGED = 'packaged'
    DELIVERING = 'delivering'
    COMPLETED = 'completed'
    FAILED = 'failed'
    STATUS_CHOICES = (
        (PACKAGING, _('打包中')),
        (PACKAGED, _('已打包')),
        (DELIVERING, _('投递中')),
        (COMPLETED, _('完成')),
        (FAILED, _('失败')),
    )

    id = models.BigAutoField(
        primary_key=True)
    users = models.ManyToManyField(
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
        blank=True,
        default='',
        max_length=255)
    file_size = models.BigIntegerField(
        verbose_name=_('附件大小'),
        default=0)
    status = models.CharField(
        verbose_name=_('投递状态'),
        default=FAILED,
        choices=STATUS_CHOICES,
        max_length=20)
    date = models.DateTimeField(
        verbose_name=_('投递时间'),
        auto_now_add=True)

    def fmt_file_size_mb(self):
        return '{:.2f}MB'.format(self.file_size / float(1024 * 1024))

    fmt_file_size_mb.short_description = _('附件大小')
    fmt_file_size_mb.admin_order_field = 'file_size'

    class Meta:
        verbose_name = _('投递日志')
        verbose_name_plural = verbose_name
