from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Custom User model con soporte para múltiples roles educativos.
    Extiende Django's AbstractUser para agregar campos específicos de la plataforma.
    """

    # Definir roles educativos
    ROLE_CHOICES = (
        ('admin', _('Administrador')),
        ('director', _('Director/Directora')),
        ('docente', _('Docente')),
        ('estudiante', _('Estudiante')),
        ('padre', _('Padre/Madre/Acudiente')),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='estudiante',
        help_text=_('Rol principal en la plataforma')
    )

    cedula = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        help_text=_('Número de cédula/identificación')
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text=_('Teléfono de contacto')
    )

    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        null=True,
        blank=True,
        help_text=_('Foto de perfil')
    )

    bio = models.TextField(
        blank=True,
        max_length=500,
        help_text=_('Biografía corta')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_('Fecha de creación de cuenta')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_('Última actualización')
    )

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['cedula']),
            models.Index(fields=['role']),
        ]

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    def get_role_display(self):
        return dict(self.ROLE_CHOICES).get(self.role, self.role)

    @property
    def is_teacher(self):
        return self.role == 'docente'

    @property
    def is_student(self):
        return self.role == 'estudiante'

    @property
    def is_parent(self):
        return self.role == 'padre'


class Institution(models.Model):
    """
    Modelo para representar instituciones educativas.
    """

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='institution_logos/', null=True, blank=True)
    address = models.CharField(max_length=500, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    admin_users = models.ManyToManyField(
        'accounts.CustomUser',
        related_name='admin_institutions',
        blank=True,
        limit_choices_to={'role__in': ['admin', 'director']},
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Institución')
        verbose_name_plural = _('Instituciones')
        ordering = ['name']
        indexes = [models.Index(fields=['slug'])]

    def __str__(self):
        return self.name


class AcademicYear(models.Model):
    """
    Modelo para gestionar años escolares/académicos.
    """

    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name='academic_years'
    )
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Año Académico')
        verbose_name_plural = _('Años Académicos')
        ordering = ['-start_date']
        constraints = [
            models.UniqueConstraint(
                fields=['institution', 'name'],
                name='unique_year_per_institution'
            )
        ]

    def __str__(self):
        return f"{self.institution.name} - {self.name}"
