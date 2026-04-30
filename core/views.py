from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Count, Avg, Q
from accounts.models import CustomUser, Institution
from academic.models import Course, Enrollment, Grade, Attendance
from administrative.models import Payment, StudentProfile


def role_required(roles):
    """Decorator to check if user has required role"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role not in roles:
                messages.error(request, 'No tienes permisos para acceder a esta página')
                return redirect('home')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


@login_required
def home(request):
    """Home view that redirects to role-specific dashboard"""
    role_dashboards = {
        'admin': '/dashboard/admin/',
        'director': '/dashboard/director/',
        'docente': '/dashboard/docente/',
        'estudiante': '/dashboard/estudiante/',
        'padre': '/dashboard/padre/',
    }
    dashboard_url = role_dashboards.get(request.user.role, '/api/docs/')
    return redirect(dashboard_url)


@login_required
@role_required(['admin'])
def admin_dashboard(request):
    """
    Admin dashboard with system-wide statistics and management
    KPIs: total users, students, teachers, courses, payments
    """
    context = {
        'total_students': CustomUser.objects.filter(role='estudiante', is_active=True).count(),
        'total_teachers': CustomUser.objects.filter(role='docente', is_active=True).count(),
        'total_courses': Course.objects.filter(is_active=True).count(),
        'total_institutions': Institution.objects.filter(is_active=True).count(),
        'pending_payments': Payment.objects.filter(
            status__in=['pending', 'overdue']
        ).count(),
        'avg_attendance': calculate_avg_attendance(),
        'avg_gpa': calculate_avg_gpa(),
    }
    return render(request, 'admin/dashboard.html', context)


@login_required
@role_required(['director'])
def director_dashboard(request):
    """
    Director dashboard with institutional overview
    """
    # Get director's institutions
    director = request.user
    institutions = Institution.objects.filter(admin_users=director)

    context = {
        'institutions': institutions,
        'total_students': CustomUser.objects.filter(
            role='estudiante',
            is_active=True
        ).count(),
        'total_teachers': CustomUser.objects.filter(
            role='docente',
            is_active=True
        ).count(),
        'total_courses': Course.objects.filter(is_active=True).count(),
        'pending_payments': Payment.objects.filter(
            status__in=['pending', 'overdue']
        ).count(),
    }
    return render(request, 'director/dashboard.html', context)


@login_required
@role_required(['docente'])
def docente_dashboard(request):
    """
    Teacher dashboard with class management and grading
    """
    teacher = request.user
    courses = Course.objects.filter(teacher=teacher, is_active=True)

    context = {
        'courses': courses,
        'total_enrollments': Enrollment.objects.filter(
            course__in=courses,
            status='active'
        ).count(),
        'pending_grades': Grade.objects.filter(
            enrollment__course__in=courses,
            score__isnull=True
        ).count(),
    }
    return render(request, 'docente/dashboard.html', context)


@login_required
@role_required(['estudiante'])
def estudiante_dashboard(request):
    """
    Student dashboard with grades, attendance, and academic progress
    """
    student = request.user
    enrollments = Enrollment.objects.filter(student=student, status='active')

    context = {
        'enrollments': enrollments,
        'gpa': calculate_student_gpa(student),
        'attendance_rate': calculate_student_attendance(student),
        'pending_tasks': 3,  # Placeholder
    }
    return render(request, 'estudiante/dashboard.html', context)


@login_required
@role_required(['padre'])
def padre_dashboard(request):
    """
    Parent dashboard with child progress monitoring
    """
    parent = request.user
    # Get children enrolled to this parent
    children = CustomUser.objects.filter(
        role='estudiante',
        student_profile__parent=parent
    )

    context = {
        'children': children,
        'total_children': children.count(),
    }
    return render(request, 'padre/dashboard.html', context)


# Helper functions for statistics

def calculate_avg_attendance():
    """Calculate system-wide average attendance percentage"""
    attendances = Attendance.objects.all()
    total = attendances.count()

    if total == 0:
        return 0

    present_count = attendances.filter(status='present').count()
    return round((present_count / total) * 100, 1)


def calculate_avg_gpa():
    """Calculate system-wide average GPA"""
    grades = Grade.objects.filter(score__isnull=False)

    if not grades.exists():
        return 0

    avg = grades.aggregate(avg_score=Avg('score'))['avg_score']
    return round(avg, 2) if avg else 0


def calculate_student_gpa(student):
    """Calculate individual student GPA"""
    enrollments = Enrollment.objects.filter(student=student)
    grades = Grade.objects.filter(
        enrollment__in=enrollments,
        score__isnull=False
    )

    if not grades.exists():
        return 0

    avg = grades.aggregate(avg_score=Avg('score'))['avg_score']
    return round(avg, 2) if avg else 0


def calculate_student_attendance(student):
    """Calculate individual student attendance percentage"""
    attendances = Attendance.objects.filter(
        enrollment__student=student
    )

    if not attendances.exists():
        return 0

    total = attendances.count()
    present = attendances.filter(status='present').count()
    return round((present / total) * 100, 1)
