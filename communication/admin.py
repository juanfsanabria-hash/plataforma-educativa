from django.contrib import admin
from accounts.admin import secure_admin
from .models import Announcement, Message, Notification


@admin.register(Announcement, site=secure_admin)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'institution', 'author', 'is_published', 'created_at')
    list_filter = ('is_published', 'institution', 'created_at')
    search_fields = ('title', 'institution__name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Message, site=secure_admin)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__email', 'recipient__email', 'subject')
    readonly_fields = ('created_at', 'read_at')


@admin.register(Notification, site=secure_admin)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__email', 'title')
    readonly_fields = ('created_at', 'read_at')
