from django.contrib import admin
from django.utils.translation import gettext_lazy as _

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
