from rest_framework import serializers
from .models import Announcement, Message, Notification


class AnnouncementSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    institution_name = serializers.CharField(source='institution.name', read_only=True)

    class Meta:
        model = Announcement
        fields = ('id', 'institution', 'institution_name', 'title', 'content',
                  'author', 'author_name', 'is_published', 'created_at', 'updated_at')
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)
    recipient_name = serializers.CharField(source='recipient.get_full_name', read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'sender_name', 'recipient', 'recipient_name',
                  'subject', 'content', 'is_read', 'created_at', 'read_at')
        read_only_fields = ('id', 'sender', 'created_at', 'read_at')


class NotificationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'user', 'user_name', 'notification_type', 'title',
                  'message', 'is_read', 'link', 'created_at', 'read_at')
        read_only_fields = ('id', 'user', 'created_at', 'read_at')
