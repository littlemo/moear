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
    taxonomy = models.CharField(
        verbose_name=_('分类'),
        unique=True,
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
        verbose_name=_('文章数统计'))

    def __str__(self):
        term_name = self.term and self.term.get('name', None)
        output = '[{id}]{term_name} => {description}'.format(
            id=self.id,
            term_name=term_name,
            description=self.description)
        return output

    class Meta:
        verbose_name = _('分类数据')
        verbose_name_plural = verbose_name
