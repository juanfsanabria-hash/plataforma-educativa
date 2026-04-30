from django.contrib import admin
from .models import StudentProfile, Payment


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'institution', 'enrollment_status', 'created_at')
    list_filter = ('institution', 'enrollment_status', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student_profile', 'concept', 'amount', 'status', 'due_date')
    list_filter = ('status', 'institution', 'due_date')
    search_fields = ('student_profile__user__email', 'concept')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Student Info', {'fields': ('student_profile', 'institution')}),
        ('Payment Details', {'fields': ('concept', 'amount', 'currency')}),
        ('Status', {'fields': ('status', 'due_date', 'paid_date', 'payment_method')}),
        ('Additional', {'fields': ('notes', 'created_at', 'updated_at')}),
    )
