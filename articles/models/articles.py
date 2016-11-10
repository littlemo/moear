from django.db import models

from .components import Source


class Article(models.Model):
    """
    文章基本信息，即保证正常逻辑执行的最小信息集
    """
    pub_datetime = models.DateTimeField(verbose_name='发布时间')
    title = models.CharField(verbose_name='标题', max_length=255)
    source = models.ForeignKey(Source, verbose_name='来源')
    url = models.CharField(verbose_name='原文URL', unique=True, max_length=255)
    local_url = models.CharField(verbose_name='本地URL', unique=True, null=True, default=None, max_length=255)

    class Meta:
        verbose_name = '文章信息'
        verbose_name_plural = verbose_name
        ordering = ('-pub_datetime',)


class ZhihuDaily(models.Model):
    """
    知乎日报模型，作为对文章类型的扩展，保存知乎日报的一些特定参数
    """
    article = models.OneToOneField(Article, on_delete=models.CASCADE, verbose_name='文章')
    daily_id = models.IntegerField(verbose_name='日报ID')
    cover_images = models.CharField(verbose_name='封面图片', null=True, default=None, max_length=255)
    top = models.BooleanField(verbose_name='热文')

    def __str__(self):
        return '[Top]' if self.top else ''

    class Meta:
        verbose_name = '知乎日报'
        verbose_name_plural = verbose_name
