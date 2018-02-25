from django.contrib.auth.models import User
from django.db import models

from .articles import Article
from .components import Tag

STAR_CHOICES = (
    (0, '-'),
    (1, '★'),
    (2, '★★'),
    (3, '★★★'),
    (4, '★★★★'),
    (5, '★★★★★'),
)


class ReadRecord(models.Model):
    """
    阅读记录模型，用于保存每位用户对阅读后的文章的打分、读后感、分类标签等信息
    """
    reader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='读者', related_name='reader')
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, verbose_name='文章')

    star = models.SmallIntegerField(verbose_name='文章评级', default=0, choices=STAR_CHOICES)
    comment = models.TextField(verbose_name='读后感', null=True, default=None)

    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')

    def fmt_tag_list(self):
        return ','.join([str(tag) for tag in Tag.objects.filter(readrecord=self)])

    fmt_tag_list.short_description = '标签列表'

    class Meta:
        verbose_name = '阅读记录'
        verbose_name_plural = verbose_name
        unique_together = ('reader', 'article')
