from django.contrib import admin


class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('文章信息', {'fields': ['title', 'source', 'pub_datetime']}),
        ('链接信息', {'fields': ['url', 'url_local', 'cover_image', 'cover_image_local']}),
    ]
    list_display = ('pub_datetime', 'source', 'title', 'fmt_url_info')

    search_fields = ['title']
    date_hierarchy = 'pub_datetime'
