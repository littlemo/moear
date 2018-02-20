from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import *


class TermAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'slug')
    search_fields = [
        'name', 'slug']


class TaxonomyAdmin(admin.ModelAdmin):
    list_display = (
        'term', 'taxonomy_type', 'description', 'parent',
        'count')
    search_fields = [
        'term__name', 'description']
    list_filter = ('taxonomy_type',)


class RelationshipsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'post', 'taxonomy', 'user')
    search_fields = [
        'post__title', 'taxonomy__term__name', 'user__username']


admin.site.register(Term, TermAdmin)
admin.site.register(Taxonomy, TaxonomyAdmin)
admin.site.register(Relationships, RelationshipsAdmin)
