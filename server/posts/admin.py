import logging

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import *
from . import tasks

log = logging.getLogger(__name__)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'fmt_spider_display_name', 'title',
        'date', 'origin_url', 'status')
    search_fields = [
        'author', 'content', 'title',
        'excerpt']
    list_filter = ('date',)
    date_hierarchy = 'date'
    readonly_fields = (
        'date', 'modified')
    actions = [
        'action_package_post']

    def action_package_post(self, request, queryset):
        '''异步打包指定文章列表'''
        post_pk_list = [post.pk for post in queryset]
        log.debug('传入的Post PK列表: {}'.format(post_pk_list))
        tasks.package_post.delay(post_pk_list)
        self.message_user(
            request,
            _('将 {num} 篇文章打包').format(
                num=len(queryset)))

    action_package_post.short_description = _('异步打包指定文章列表')


class PostMetaAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'post', 'name', 'value')
    search_fields = [
        'post__title', 'name', 'value']


class ReadRecordAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'post', 'user', 'star', 'comment')
    search_fields = [
        'post__title', 'user__username', 'star',
        'comment']


admin.site.register(Post, PostAdmin)
admin.site.register(PostMeta, PostMetaAdmin)
admin.site.register(ReadRecord, ReadRecordAdmin)
