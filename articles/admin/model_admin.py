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

    # FIXME 此处通过article__pub_datetime的搜索会存在时区Bug，即搜索时需使用0时区而非本地时区才能搜索到
    search_fields = ['article__title', 'article__pub_datetime']
    list_filter = ['top']


class TagAdmin(admin.ModelAdmin):
    list_display = ('theme', 'creator')
    search_fields = ['theme']


class SourceAdmin(admin.ModelAdmin):
    fieldsets = [
        ('组件信息', {'fields': ['name', 'verbose_name', 'author', 'description']}),
        ('配置信息', {'fields': ['persistent']}),
    ]
    list_display = ('name', 'verbose_name', 'author', 'description', 'persistent')
    readonly_fields = ('name', 'verbose_name', 'author', 'description')


class ReadRecordAdmin(admin.ModelAdmin):
    fieldsets = [
        ('阅读记录', {'fields': ['reader', 'article']}),
        ('打分评论', {'fields': ['star', 'comment']}),
        ('标签分类', {'fields': ['tags']}),
    ]
    list_display = ('reader', 'article', 'star', 'comment', 'fmt_tag_list')
    list_filter = ('reader', 'tags')

    filter_horizontal = ('tags',)
    # readonly_fields = ('reader', 'article')
