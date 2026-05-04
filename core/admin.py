from django.contrib import admin
from accounts.admin import secure_admin
from .models import ScheduleEvent


class ScheduleEventAdmin(admin.ModelAdmin):
    list_display      = ('title', 'event_type', 'start', 'end', 'created_by', 'institution')
    list_filter       = ('event_type', 'institution', 'start')
    search_fields     = ('title', 'description')
    filter_horizontal = ('attendees',)


secure_admin.register(ScheduleEvent, ScheduleEventAdmin)
