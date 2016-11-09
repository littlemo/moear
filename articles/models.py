from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html


class Tag(models.Model):
    theme = models.CharField(verbose_name='主题', max_length=50, unique=True)

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


class ZhihuDaily(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, verbose_name='文章')
    daily_id = models.IntegerField(verbose_name='日报ID')
    cover_images = models.CharField(verbose_name='封面图片', null=True, default=None, max_length=255)
    top = models.BooleanField(verbose_name='热文')

    def __str__(self):
        return self.article

    def fmt_tags_list(self):
        return '，'.join([str(tag) for tag in Tag.objects.filter(article__pk=self.pk)])

    class Meta:
        verbose_name = '知乎日报'
        verbose_name_plural = verbose_name


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
