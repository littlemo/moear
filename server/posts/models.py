from django.db import models
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    """
    文章数据模型

    该应用的核心模型，用于存储数据源抓取的文章实体
    """
    STATUS_CHOICES = (
        ('publish', _('发布')),
        ('private', _('私有')),
    )
    # COMMENT_STATUS_CHOICES = (
    #     ('open', _('开启')),
    #     ('closed', _('关闭')),
    # )

    id = models.BigAutoField(
        db_index=True,
        primary_key=True)
    author = models.CharField(
        verbose_name=_('作者'),
        blank=True,
        default='',
        max_length=255)
    spider = models.ForeignKey(
        'spiders.Spider',
        verbose_name=_('爬虫信息'),
        db_index=True,
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_NULL)
    origin_url = models.CharField(
        verbose_name='原文地址',
        unique=True,
        max_length=255)
    date = models.DateTimeField(
        verbose_name=_('发布时间'),
        db_index=True,
        auto_now_add=True)
    content = models.TextField(
        verbose_name=_('文章正文'))
    title = models.CharField(
        verbose_name=_('文章标题'),
        max_length=65535)
    excerpt = models.CharField(
        verbose_name=_('文章摘要'),
        blank=True,
        null=True,
        max_length=65535)
    status = models.CharField(
        verbose_name=_('文章状态'),
        db_index=True,
        default='publish',
        choices=STATUS_CHOICES,
        max_length=20)
    # comment_status = models.CharField(
    #     verbose_name=_('评论状态'),
    #     default='open',
    #     choices=COMMENT_STATUS_CHOICES,
    #     max_length=20)
    modified = models.DateTimeField(
        verbose_name=_('修改时间'),
        auto_now=True)
    # comment_count = models.BigIntegerField(
    #     verbose_name=_('评论总数'),
    #     default=0)

    def __str__(self):
        output = '[{source}]{title}'.format(
            source=self.source,
            title=self.title)
        return output

    class Meta:
        verbose_name = _('文章数据')
        verbose_name_plural = verbose_name


class PostMeta(models.Model):
    """
    文章元数据模型

    用于存储指定文章的元数据信息，便于插件&爬虫实现扩展功能
    """
    id = models.BigAutoField(
        primary_key=True)
    post = models.ForeignKey(
        'Post',
        verbose_name=_('文章数据'),
        db_index=True,
        on_delete=models.CASCADE)
    key = models.CharField(
        verbose_name=_('键名'),
        db_index=True,
        blank=True,
        null=True,
        default=None,
        max_length=255)
    value = models.TextField(
        verbose_name=_('键名'),
        blank=True,
        null=True,
        default=None)
