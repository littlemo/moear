from django.db import models


class Tag(models.Model):
    theme = models.CharField(verbose_name='主题', max_length=50, unique=True)

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = '文章主题'
        verbose_name_plural = verbose_name


class Source(models.Model):
    name = models.CharField(verbose_name='来源名称', max_length=50, unique=True)
    # TODO V2.1.0 增加爬取时间规则时，在此处增加相应的 `rules` 属性

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '文章来源'
        verbose_name_plural = verbose_name
