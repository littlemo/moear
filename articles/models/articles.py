from django.db import models

from .components import Source


class Article(models.Model):
    pub_datetime = models.DateTimeField(verbose_name='发布时间')
    title = models.CharField(verbose_name='标题', max_length=255)
    source = models.ForeignKey(Source, verbose_name='来源')
    url = models.CharField(verbose_name='原文URL', unique=True, max_length=255)
    local_url = models.CharField(verbose_name='本地URL', unique=True, null=True, default=None, max_length=255)

    class Meta:
        verbose_name = '文章基本'
        verbose_name_plural = verbose_name
        ordering = ('-pub_datetime',)


class ZhihuDaily(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, verbose_name='文章')
    daily_id = models.IntegerField(verbose_name='日报ID')
    cover_images = models.CharField(verbose_name='封面图片', null=True, default=None, max_length=255)
    top = models.BooleanField(verbose_name='热文')

    def __str__(self):
        return self.article

    class Meta:
        verbose_name = '知乎日报'
        verbose_name_plural = verbose_name
