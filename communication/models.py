from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser, Institution


class Announcement(models.Model):
    """Institution-wide announcements"""
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='announcements_created')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Anuncio')
        verbose_name_plural = _('Anuncios')
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Message(models.Model):
    """Direct messages between users"""
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Mensaje')
        verbose_name_plural = _('Mensajes')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender.get_full_name()} → {self.recipient.get_full_name()}"


class Notification(models.Model):
    """System notifications for users"""
    NOTIFICATION_TYPES = [
        ('grade', _('Calificación')),
        ('attendance', _('Asistencia')),
        ('payment', _('Pago')),
        ('message', _('Mensaje')),
        ('announcement', _('Anuncio')),
        ('system', _('Sistema')),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Notificación')
        verbose_name_plural = _('Notificaciones')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.title}"
