from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html


STAR_CHOICES = (
    (0, '-'),
    (1, '★'),
    (2, '★★'),
    (3, '★★★'),
    (4, '★★★★'),
    (5, '★★★★★'),
)


class ReadRecord(models.Model):
    reader = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='读者')
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, verbose_name='文章')
    star = models.SmallIntegerField(verbose_name='文章评级', default=0, choices=STAR_CHOICES)
    comment = models.TextField(verbose_name='读后感', null=True, default=None)

    class Meta:
        verbose_name = '阅读记录'
        verbose_name_plural = verbose_name
