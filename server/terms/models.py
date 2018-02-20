from django.db import models
from django.utils.translation import gettext_lazy as _


class Term(models.Model):
    """
    术语数据模型

    用于存储所有术语字段及其slug
    """
    id = models.BigAutoField(
        primary_key=True)
    name = models.CharField(
        verbose_name=_('术语名'),
        unique=True,
        max_length=200)
    slug = models.CharField(
        verbose_name=_('Slug'),
        unique=True,
        max_length=200)

    def __str__(self):
        output = '[{id}]{name} => {slug}'.format(
            id=self.id,
            name=self.name,
            slug=self.slug)
        return output

    class Meta:
        verbose_name = _('术语数据')
        verbose_name_plural = verbose_name


class Taxonomy(models.Model):
    """
    分类模型

    用于关联术语，为术语数据提供扩展属性定义
    """
    id = models.BigAutoField(
        primary_key=True)
    term = models.OneToOneField(
        'Term',
        verbose_name=_('术语'),
        db_index=True,
        on_delete=models.CASCADE)
    taxonomy_type = models.CharField(
        verbose_name=_('分类类型'),
        max_length=32)
    description = models.TextField(
        blank=True,
        default='',
        verbose_name=_('描述'))
    parent = models.ForeignKey(
        'Taxonomy',
        verbose_name=_('父分类'),
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_NULL)
    count = models.BigIntegerField(
        verbose_name=_('文章计数'),
        blank=True,
        default=0)

    def __str__(self):
        output = '[{id}]{term_name}'.format(
            id=self.id,
            term_name=self.term.name)
        if self.description:
            output += ' => {description}'.format(
                description=self.description)
        return output

    class Meta:
        verbose_name = _('分类数据')
        verbose_name_plural = verbose_name


class Relationships(models.Model):
    """
    分类关系模型

    存储文章与对应分类的映射关系
    """
    id = models.BigAutoField(
        primary_key=True)
    post = models.ForeignKey(
        'posts.Post',
        verbose_name=_('文章数据'),
        db_index=True,
        on_delete=models.CASCADE)
    taxonomy = models.ForeignKey(
        'Taxonomy',
        verbose_name=_('分类'),
        db_index=True,
        on_delete=models.CASCADE)
    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('用户'),
        db_index=True,
        on_delete=models.CASCADE)

    def __str__(self):
        output = '[{id}][{username}][{term_name}] {post_title}'.format(
            id=self.id,
            username=self.user.auto_created,
            term_name=self.taxonomy.term.name,
            post_title=self.post.title)
        return output

    class Meta:
        verbose_name = _('分类关系')
        verbose_name_plural = verbose_name
        unique_together = ('post', 'taxonomy', 'user')
