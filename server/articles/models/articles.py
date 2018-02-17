from django.db import models
from django.utils import timezone
from django.utils.html import format_html

from .components import Source


class Article(models.Model):
    """
    文章基本信息，即保证正常逻辑执行的最小信息集
    """
    pub_datetime = models.DateTimeField(verbose_name='发布时间')
    title = models.CharField(verbose_name='标题', max_length=255)
    source = models.ForeignKey(Source, verbose_name='来源', on_delete=models.SET_NULL)
    url = models.CharField(verbose_name='原文URL', unique=True, max_length=255)
    url_local = models.CharField(verbose_name='本地URL', unique=True, null=True, default=None, max_length=255)
    cover_image = models.CharField(verbose_name='封面图片', null=True, default=None, max_length=255)
    cover_image_local = models.CharField(verbose_name='封面图片本地', null=True, default=None, max_length=255)

    def fmt_url_info(self):
        display = '<a href="{}" target="_blank">原文</a>'.format(self.url)
        display += '(<a href="/articles/{}" target="_blank">本地</a>)'.format(self.url_local)
        # display += ' |'
        # display += ' <a href="{}" target="_blank">封面</a>'.format(self.cover_image)
        # display += ' <a href="/articles/{}" target="_blank">封面</a>'.format(self.cover_image_local)
        return format_html(display)

    fmt_url_info.short_description = '链接信息'

    def __str__(self):
        tz = timezone.get_current_timezone()
        return '<{}>{}'.format(timezone.datetime.fromtimestamp(
            self.pub_datetime.timestamp(), tz=tz).strftime('%Y-%m-%d'), self.title)

    class Meta:
        verbose_name = '文章信息'
        verbose_name_plural = verbose_name
        ordering = ('-pub_datetime',)


class ZhihuDaily(models.Model):
    """
    知乎日报模型，作为对文章类型的扩展，保存知乎日报的一些特定参数
    """
    article = models.OneToOneField(Article, on_delete=models.CASCADE, verbose_name='文章')
    daily_id = models.IntegerField(verbose_name='日报ID', unique=True)
    top = models.BooleanField(verbose_name='热文')

    def __str__(self):
        return '[Top]' if self.top else ''

    class Meta:
        verbose_name = '知乎日报'
        verbose_name_plural = verbose_name
