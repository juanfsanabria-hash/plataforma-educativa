from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser, Institution, AcademicYear


class StudentProfile(models.Model):
    """Extended student profile with administrative info"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                               limit_choices_to={'role': 'estudiante'},
                               related_name='student_profile')
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT, related_name='students')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=[
        ('M', _('Masculino')),
        ('F', _('Femenino')),
        ('O', _('Otro')),
    ], blank=True)
    address = models.CharField(max_length=500, blank=True)
    emergency_contact = models.CharField(max_length=255, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    parent = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children_profiles',
        limit_choices_to={'role': 'padre'},
    )
    parent_names = models.TextField(blank=True)
    enrollment_status = models.CharField(max_length=20, choices=[
        ('active', _('Activo')),
        ('inactive', _('Inactivo')),
        ('graduated', _('Graduado')),
        ('dropped', _('Retirado')),
    ], default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Perfil Estudiante')
        verbose_name_plural = _('Perfiles Estudiante')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.institution.name}"


class Payment(models.Model):
    """Payment/Financial transactions"""
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='payments')
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='payments')
    concept = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='COP')
    status = models.CharField(max_length=20, choices=[
        ('pending', _('Pendiente')),
        ('partially_paid', _('Parcialmente pagado')),
        ('paid', _('Pagado')),
        ('overdue', _('Vencido')),
        ('waived', _('Condonado')),
    ], default='pending')
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=[
        ('transfer', _('Transferencia')),
        ('cash', _('Efectivo')),
        ('check', _('Cheque')),
        ('card', _('Tarjeta')),
        ('other', _('Otro')),
    ], blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Pago')
        verbose_name_plural = _('Pagos')
        ordering = ['due_date']

    def __str__(self):
        return f"{self.student_profile.user.get_full_name()} - {self.concept} ({self.status})"
