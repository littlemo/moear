from django.contrib.auth.models import User
from django.db import models

from .components import Source


class SubscribeInfo(models.Model):
    """
    用户订阅信息，包含要推送的文章源，目标邮箱地址，以及推送时间规则
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='读者')
    source = models.ForeignKey(Source, on_delete=models.CASCADE, verbose_name='文章来源')
    push_address = models.CharField(verbose_name='推送地址', max_length=255, help_text="多邮箱使用';'分隔")
    rules = models.CharField(verbose_name='推送规则', max_length=255)

    class Meta:
        verbose_name = '订阅信息'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'source')
