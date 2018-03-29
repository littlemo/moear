import logging
import stevedore

from django.contrib import admin
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .models import Post, PostMeta, ReadRecord
from . import tasks
from deliver.tasks import deliver_book_task

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
        'action_package_post',
        'action_deliver_book',
        'action_package_deliver',
    ]

    def action_package_post(self, request, queryset):
        '''异步打包指定文章列表'''
        post_pk_list = [post.pk for post in queryset]
        log.info('待打包的文章PK列表: {}'.format(post_pk_list))
        tasks.package_post.delay(post_pk_list, dispatch=False)
        self.message_user(
            request,
            _('将 {num} 篇文章打包').format(
                num=len(queryset)))

    def action_deliver_book(self, request, queryset):
        '''异步投递书籍文件到设备'''
        import os
        from .utils import \
            trans_to_package_group, posts_list_md5, yield_sec_level_dict

        post_pk_list = [post.pk for post in queryset]
        package_group = trans_to_package_group(post_pk_list)
        for package_module, spider_name, book_group \
                in yield_sec_level_dict(package_group):
            spider_dict = book_group.get('spider', {})
            posts_data_raw = book_group.get('data', [])
            package_mgr = stevedore.driver.DriverManager(
                namespace='moear.package',
                name=package_module,
                invoke_on_load=True,
                invoke_args=(spider_dict,),
            )
            book_ext = package_mgr.driver.ext
            book_filename = \
                '{spider_display_name}[{publish_date}]_{md5}.{ext}'.format(
                    spider_display_name=spider_dict.get('display_name'),
                    publish_date=posts_data_raw[0].get('date').split('T')[0],
                    md5=posts_list_md5(posts_data_raw),
                    ext=book_ext,
                )
            book_abspath = os.path.join(
                settings.BOOK_PACKAGE_ROOT, book_filename)
            deliver_book_task.delay(
                [request.user.email],
                book_filename.split('_')[0],
                book_abspath)

    def action_package_deliver(self, request, queryset):
        '''异步打包并投递书籍'''
        post_pk_list = [post.pk for post in queryset]
        log.info('待打包并投递的文章PK列表: {}'.format(post_pk_list))
        tasks.package_post.delay(post_pk_list)
        self.message_user(
            request,
            _('将 {num} 篇文章打包并投递').format(
                num=len(queryset)))

    action_package_post.short_description = _('异步打包指定文章列表')
    action_deliver_book.short_description = _('异步投递书籍文件')
    action_package_deliver.short_description = _('异步打包并投递书籍')


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
