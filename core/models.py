from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser, Institution


class ScheduleEvent(models.Model):
    EVENT_TYPES = [
        ('class',        _('Clase')),
        ('evaluation',   _('Evaluación')),
        ('task',         _('Tarea')),
        ('meeting',      _('Reunión')),
        ('holiday',      _('Festivo/Vacaciones')),
        ('announcement', _('Anuncio')),
    ]

    created_by  = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='created_events'
    )
    attendees   = models.ManyToManyField(
        CustomUser, blank=True, related_name='events'
    )
    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE,
        related_name='events', null=True, blank=True
    )
    event_type  = models.CharField(max_length=20, choices=EVENT_TYPES, default='class')
    title       = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start       = models.DateTimeField()
    end         = models.DateTimeField()
    all_day     = models.BooleanField(default=False)
    color       = models.CharField(max_length=7, default='#3b82f6')
    course_id   = models.PositiveIntegerField(null=True, blank=True)
    url             = models.CharField(max_length=500, blank=True)
    study_material  = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Evento')
        verbose_name_plural = _('Eventos')
        ordering = ['start']
        indexes = [
            models.Index(fields=['start', 'end']),
            models.Index(fields=['event_type']),
        ]

    def __str__(self):
        return f"[{self.get_event_type_display()}] {self.title} — {self.start:%Y-%m-%d %H:%M}"
