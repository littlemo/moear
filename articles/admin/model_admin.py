from django.contrib import admin


class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('文章信息', {'fields': ['title', 'source', 'pub_datetime']}),
        ('链接信息', {'fields': ['url', 'url_local', 'cover_image', 'cover_image_local']}),
    ]
    list_display = ('pub_datetime', 'source', 'title', 'fmt_url_info')

    search_fields = ['title']
    date_hierarchy = 'pub_datetime'


class ZhihuDailyAdmin(admin.ModelAdmin):
    fieldsets = [
        ('基础文章', {'fields': ['article']}),
        ('扩展信息', {'fields': ['daily_id', 'top']}),
    ]
    list_display = ('daily_id', 'article', 'top')
    readonly_fields = ('article',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('theme', 'creater')


class SourceAdmin(admin.ModelAdmin):
    fieldsets = [
        ('组件信息', {'fields': ['name', 'verbose_name', 'author', 'description']}),
        ('配置信息', {'fields': ['persistent']}),
    ]
    list_display = ('name', 'verbose_name', 'author', 'description', 'persistent')
    readonly_fields = ('name', 'verbose_name', 'author', 'description')
