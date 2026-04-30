from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Announcement, Message, Notification
from .serializers import AnnouncementSerializer, MessageSerializer, NotificationSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    """API endpoints for announcements"""
    queryset = Announcement.objects.filter(is_published=True)
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['institution', 'is_published']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at']


class MessageViewSet(viewsets.ModelViewSet):
    """API endpoints for messages"""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['subject', 'content']
    ordering_fields = ['created_at']

    def get_queryset(self):
        user = self.request.user
        # Users see messages they sent or received
        return Message.objects.filter(sender=user) | Message.objects.filter(recipient=user)


class NotificationViewSet(viewsets.ModelViewSet):
    """API endpoints for notifications"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['notification_type', 'is_read']
    search_fields = ['title', 'message']
    ordering_fields = ['created_at']

    def get_queryset(self):
        # Users only see their own notifications
        return Notification.objects.filter(user=self.request.user)
