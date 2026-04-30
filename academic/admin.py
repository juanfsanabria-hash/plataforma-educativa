from django.contrib import admin
from .models import Course, Enrollment, Grade, Attendance


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution', 'academic_year', 'teacher', 'is_active')
    list_filter = ('institution', 'academic_year', 'is_active', 'teacher')
    search_fields = ('name', 'institution__name')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'enrolled_date')
    list_filter = ('status', 'course__academic_year', 'enrolled_date')
    search_fields = ('student__email', 'course__name')
    readonly_fields = ('enrolled_date', 'created_at')


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'evaluation_name', 'evaluation_type', 'score')
    list_filter = ('evaluation_type', 'recorded_date')
    search_fields = ('enrollment__student__email', 'evaluation_name')
    readonly_fields = ('recorded_date',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'date', 'status', 'recorded_by')
    list_filter = ('status', 'date', 'recorded_by')
    search_fields = ('enrollment__student__email',)
    readonly_fields = ('created_at',)
