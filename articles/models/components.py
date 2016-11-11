from django.db import models

from django.contrib.auth.models import User


class Tag(models.Model):
    """
    文章标签，用户给已阅文章增加的分类标签
    """
    theme = models.CharField(verbose_name='主题', max_length=50, unique=True)
    creater = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = '文章主题'
        verbose_name_plural = verbose_name


class Source(models.Model):
    """
    文章源组件，用来指示文章来源的名称，以及未来的爬取规则&方法
    """
    name = models.CharField(verbose_name='来源名称', max_length=50, unique=True)
    localization = models.BooleanField(verbose_name='文章本地化')
    # TODO V2.1.0 增加爬取时间规则时，在此处增加相应的 `rules` 属性

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '文章来源'
        verbose_name_plural = verbose_name
