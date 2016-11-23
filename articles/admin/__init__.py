from django.contrib import admin

from articles.models import *

from .model_admin import ArticleAdmin
from .model_admin import ZhihuDailyAdmin
from .model_admin import TagAdmin
from .model_admin import SourceAdmin
from .model_admin import ReadRecordAdmin

admin.site.register(Article, ArticleAdmin)
admin.site.register(ZhihuDaily, ZhihuDailyAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(ReadRecord, ReadRecordAdmin)

admin.AdminSite.site_header = '貘耳朵管理系统'
admin.AdminSite.site_title = '貘耳朵'
admin.AdminSite.index_title = '站点管理'
