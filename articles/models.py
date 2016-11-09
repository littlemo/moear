from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html


class Tag(models.Model):
    theme = models.CharField(verbose_name='主题',
                             max_length=50,
                             unique=True)

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = '文章主题'
        verbose_name_plural = verbose_name
