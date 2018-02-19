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
