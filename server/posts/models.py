from django.db import models
from django.utils import timezone
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
        default=timezone.now)
    content = models.TextField(
        verbose_name=_('文章正文'))
    title = models.CharField(
        verbose_name=_('文章标题'),
        max_length=3000)
    excerpt = models.CharField(
        verbose_name=_('文章摘要'),
        blank=True,
        default='',
        max_length=5000)
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

    def fmt_spider_display_name(self):
        return self.spider.display_name

    fmt_spider_display_name.short_description = '爬虫名称'

    def __str__(self):
        output = '[{id}][{spider_name}]{title}'.format(
            id=self.id,
            spider_name=self.spider and self.spider.name,
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
    name = models.CharField(
        verbose_name=_('键名'),
        db_index=True,
        max_length=255)
    value = models.TextField(
        verbose_name=_('键值'),
        blank=True,
        default='')

    def __str__(self):
        output = '[{id}][{post_id}]{name} => {value}'.format(
            id=self.id,
            post_id=self.post.id,
            name=self.name,
            value=self.value)
        return output

    class Meta:
        verbose_name = _('文章元数据')
        verbose_name_plural = verbose_name


class ReadRecord(models.Model):
    """
    阅读记录数据模型

    用于保存指定用户对阅读后的文章的打分、读后感等基础信息
    """
    STAR_CHOICES = (
        (0, '-'),
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'))

    id = models.BigAutoField(
        primary_key=True)
    post = models.ForeignKey(
        'Post',
        verbose_name=_('文章数据'),
        db_index=True,
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_NULL)
    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('用户'),
        db_index=True,
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_NULL)
    star = models.SmallIntegerField(
        verbose_name=_('评级'),
        default=0,
        choices=STAR_CHOICES)
    comment = models.TextField(
        verbose_name=_('读后感'),
        blank=True,
        default='')

    def __str__(self):
        post_title = self.post and self.post.get('title', None)
        output = '[{id}][{user}][{post_title}] => {star}'.format(
            id=self.id,
            user=self.user,
            post_title=post_title,
            star=self.star)
        return output

    class Meta:
        verbose_name = _('阅读记录')
        verbose_name_plural = verbose_name
        unique_together = ('post', 'user')
