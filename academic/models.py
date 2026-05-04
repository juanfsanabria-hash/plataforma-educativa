from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser, Institution, AcademicYear


class Course(models.Model):
    """Represents a course/subject in an academic year"""
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='courses')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    credits = models.PositiveIntegerField(default=1)
    teacher = models.ForeignKey(CustomUser, on_delete=models.PROTECT,
                               limit_choices_to={'role': 'docente'},
                               related_name='taught_courses')
    schedule_description = models.CharField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Curso')
        verbose_name_plural = _('Cursos')
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['institution', 'academic_year', 'slug'],
                                   name='unique_course_per_year')
        ]

    def __str__(self):
        return f"{self.name} ({self.academic_year.name})"


class Enrollment(models.Model):
    """Student enrollment in a course"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               limit_choices_to={'role': 'estudiante'},
                               related_name='enrollments')
    enrolled_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('active', _('Activo')),
        ('dropped', _('Retirado')),
        ('transferred', _('Transferido')),
    ], default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Inscripción')
        verbose_name_plural = _('Inscripciones')
        constraints = [
            models.UniqueConstraint(fields=['course', 'student'], name='unique_enrollment')
        ]

    def __str__(self):
        return f"{self.student.get_full_name()} en {self.course.name}"


class Grade(models.Model):
    """Student grade/calification in a course"""
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='grades')
    evaluation_name = models.CharField(max_length=255)
    evaluation_type = models.CharField(max_length=50, choices=[
        ('exam', _('Examen')),
        ('quiz', _('Quiz')),
        ('assignment', _('Tarea')),
        ('project', _('Proyecto')),
        ('participation', _('Participación')),
        ('other', _('Otro')),
    ])
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    recorded_date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = _('Calificación')
        verbose_name_plural = _('Calificaciones')
        ordering = ['recorded_date']

    def percentage(self):
        if self.max_score and self.max_score > 0:
            return round(float(self.score / self.max_score) * 100, 2)
        return 0

    def __str__(self):
        return f"{self.enrollment.student.get_full_name()} - {self.evaluation_name}: {self.score}"


class Attendance(models.Model):
    """Track student attendance"""
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('present', _('Presente')),
        ('absent', _('Ausente')),
        ('late', _('Llegada tarde')),
        ('excused', _('Ausencia justificada')),
    ])
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT,
                                   limit_choices_to={'role': 'docente'})
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Asistencia')
        verbose_name_plural = _('Asistencias')
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(fields=['enrollment', 'date'], name='unique_attendance_per_day')
        ]

    def __str__(self):
        return f"{self.enrollment.student.get_full_name()} - {self.date}"


class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=255, verbose_name=_('Título'))
    description = models.TextField(blank=True, verbose_name=_('Descripción'))
    order = models.PositiveIntegerField(default=0, verbose_name=_('Orden'))
    date = models.DateField(null=True, blank=True, verbose_name=_('Fecha'))
    is_published = models.BooleanField(default=False, verbose_name=_('Publicado'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Tema')
        verbose_name_plural = _('Temas')
        ordering = ['order', 'date', 'id']

    def __str__(self):
        return f"{self.course.name} — {self.order}. {self.title}"


class TopicMaterial(models.Model):
    MATERIAL_TYPES = [
        ('file', _('Archivo')),
        ('link', _('Enlace')),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=255, verbose_name=_('Título'))
    material_type = models.CharField(max_length=10, choices=MATERIAL_TYPES, verbose_name=_('Tipo'))
    file = models.FileField(
        upload_to='materials/%Y/%m/', null=True, blank=True, verbose_name=_('Archivo')
    )
    url = models.URLField(blank=True, verbose_name=_('URL'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Material')
        verbose_name_plural = _('Materiales')
        ordering = ['created_at']

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.material_type == 'file' and not self.file:
            raise ValidationError({'file': 'Se requiere un archivo para materiales de tipo "Archivo".'})
        if self.material_type == 'link' and not self.url:
            raise ValidationError({'url': 'Se requiere una URL para materiales de tipo "Enlace".'})

    def __str__(self):
        return f"{self.topic.title} — {self.title}"
