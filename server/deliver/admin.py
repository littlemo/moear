from django.contrib import admin

from .models import DeliverLog


class DeliverLogAdmin(admin.ModelAdmin):
    list_display = (
        'date', 'spider', 'file_name', 'file_size', 'status')
    search_fields = [
        'file_name']
    list_filter = ('date',)
    date_hierarchy = 'date'


admin.site.register(DeliverLog, DeliverLogAdmin)
