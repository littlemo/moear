from django.contrib import admin

from .models import DeliverLog


class DeliverLogAdmin(admin.ModelAdmin):
    list_display = (
        'date', 'spider', 'file_name', 'fmt_file_size_mb', 'status')
    search_fields = [
        'file_name']
    list_filter = ('date',)
    date_hierarchy = 'date'


admin.site.register(DeliverLog, DeliverLogAdmin)
