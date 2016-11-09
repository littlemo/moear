from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html


class Tag(models.Model):
    theme = models.CharField(verbose_name='主题',
                             max_length=50,
                             unique=True)

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = '文章主题'
        verbose_name_plural = verbose_name


class Article(models.Model):
    pub_datetime = models.DateTimeField(verbose_name='发布时间')
    title = models.CharField(verbose_name='标题',
                             max_length=255)
    local_url = models.CharField(verbose_name='本地URL',
                                 unique=True,
                                 max_length=255)

    tags = models.ManyToManyField(Tag,
                                  blank=True,
                                  verbose_name='标签')

    class Meta:
        verbose_name = '文章基本'
        verbose_name_plural = verbose_name
        ordering = ('-pub_datetime',)
