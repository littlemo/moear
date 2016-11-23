from django.contrib import admin

from articles.models import *

from .model_admin import ArticleAdmin
from .model_admin import ZhihuDailyAdmin

admin.site.register(Article, ArticleAdmin)
admin.site.register(ZhihuDaily, ZhihuDailyAdmin)

admin.AdminSite.site_header = '貘耳朵管理系统'
admin.AdminSite.site_title = '貘耳朵'
admin.AdminSite.index_title = '站点管理'
