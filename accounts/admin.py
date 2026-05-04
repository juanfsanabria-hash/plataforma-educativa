from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Institution, AcademicYear


class SecureAdminSite(AdminSite):
    site_header = "Plataforma Educativa — Admin"
    site_title = "Admin"

    def has_permission(self, request):
        return request.user.is_active and request.user.is_superuser


secure_admin = SecureAdminSite(name='secure_admin')


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Educational Info', {'fields': ('role', 'cedula', 'phone', 'profile_photo', 'bio')}),
    )
    list_display = ('email', 'get_full_name', 'role', 'cedula', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'created_at')
    search_fields = ('email', 'first_name', 'last_name', 'cedula')
    ordering = ('-created_at',)


class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'email', 'phone', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'slug', 'email')
    prepopulated_fields = {'slug': ('name',)}


class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution', 'year', 'start_date', 'end_date', 'is_active')
    list_filter = ('institution', 'is_active', 'start_date')
    search_fields = ('name', 'institution__name')
    readonly_fields = ('created_at',)


secure_admin.register(CustomUser, CustomUserAdmin)
secure_admin.register(Institution, InstitutionAdmin)
secure_admin.register(AcademicYear, AcademicYearAdmin)
