from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import *


class SpiderAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'display_name', 'author',
        'email', 'description', 'enabled')
    search_fields = [
        'name', 'display_name', 'author',
        'email', 'description']
    list_filter = ('author',)


class SpiderMetaAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'spider', 'name', 'value')
    search_fields = [
        'spider__name', 'name', 'value']


admin.site.register(Spider, SpiderAdmin)
admin.site.register(SpiderMeta, SpiderMetaAdmin)
