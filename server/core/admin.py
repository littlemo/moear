from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required

from .models import *


class OptionAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'value', 'autoload')
    search_fields = [
        'name', 'value']


class UserMetaAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'name', 'value')
    search_fields = [
        'user__username', 'name', 'value']


admin.site.register(Option, OptionAdmin)
admin.site.register(UserMeta, UserMetaAdmin)

admin.AdminSite.site_header = _('MoEar 后台管理')
admin.AdminSite.site_title = _('MoEar')
admin.AdminSite.index_title = _('站点管理')

# 强制 admin 使用 AllAuth 的 login 策略
admin.site.login = login_required(admin.site.login)
