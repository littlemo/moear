from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import *
from . import tasks
from celery import group
from core.tasks import periodic_chain_crawl_package_deliver


class SpiderAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'display_name', 'author',
        'email', 'description', 'enabled')
    search_fields = [
        'name', 'display_name', 'author',
        'email', 'description']
    list_filter = ('author',)
    actions = [
        'action_spider_post',
        'action_periodic_chain_crawl_package_deliver',
    ]

    def action_spider_post(self, request, queryset):
        """异步爬取Post信息"""
        c = (group(
            tasks.spider_post.s(spider.name) for spider in queryset
        ))
        c.delay()
        self.message_user(
            request,
            _('共触发 {num} 个爬虫源').format(
                num=len(queryset)))

    def action_periodic_chain_crawl_package_deliver(self, request, queryset):
        '''异步周期链式爬取、打包并投递书籍'''
        c = (group(
            periodic_chain_crawl_package_deliver.s(
                spider.name) for spider in queryset
        ))
        c.delay()
        self.message_user(request, _('成功创建调用任务'))

    action_spider_post.short_description = _('异步爬取Post信息')
    action_periodic_chain_crawl_package_deliver.short_description = \
        _('异步周期链式爬取、打包并投递书籍')


class SpiderMetaAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'spider', 'name', 'value')
    search_fields = [
        'spider__name', 'name', 'value']


admin.site.register(Spider, SpiderAdmin)
admin.site.register(SpiderMeta, SpiderMetaAdmin)
