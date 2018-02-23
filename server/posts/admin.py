from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'spider', 'origin_url',
        'date', 'title',
        'status', 'modified')
    search_fields = [
        'author', 'content', 'title',
        'excerpt']
    list_filter = ('date',)
    date_hierarchy = 'date'
    readonly_fields = (
        'date', 'modified')


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
