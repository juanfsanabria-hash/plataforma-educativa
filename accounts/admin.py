from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Institution, AcademicYear


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Educational Info', {'fields': ('role', 'cedula', 'phone', 'profile_photo', 'bio')}),
    )
    list_display = ('email', 'get_full_name', 'role', 'cedula', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'created_at')
    search_fields = ('email', 'first_name', 'last_name', 'cedula')
    ordering = ('-created_at',)


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'email', 'phone', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'slug', 'email')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution', 'year', 'start_date', 'end_date', 'is_active')
    list_filter = ('institution', 'is_active', 'start_date')
    search_fields = ('name', 'institution__name')
    readonly_fields = ('created_at',)
