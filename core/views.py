from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.db.models import Count, Avg, Q
from django.db import models as db_models
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_http_methods
from django import forms as django_forms
from accounts.models import CustomUser, Institution
from communication.models import Notification
from accounts.forms import LoginForm, RegisterForm
from academic.models import Course, Enrollment, Grade, Attendance, Topic, TopicMaterial
from administrative.models import Payment, StudentProfile
from .models import ScheduleEvent


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


@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Login view with email/password authentication.
    GET: Display login form
    POST: Authenticate user and create session
    """
    # Redirect if already authenticated
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Handle "remember me"
            if form.cleaned_data.get('remember_me'):
                request.session.set_expiry(60 * 60 * 24 * 30)  # 30 días
            else:
                request.session.set_expiry(0)  # Browser close

            messages.success(request, f'¡Bienvenido {user.get_full_name()}!')
            return redirect('home')
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = LoginForm()

    context = {
        'form': form,
        'page_title': 'Iniciar Sesión',
    }
    return render(request, 'auth/login.html', context)


@require_http_methods(["GET", "POST"])
def register_view(request):
    """
    Registration view for new users.
    GET: Display registration form
    POST: Create new user account
    """
    # Redirect if already authenticated
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Create user
            user = form.save()

            # Send welcome message
            messages.success(
                request,
                f'¡Cuenta creada exitosamente! Por favor inicia sesión.'
            )

            # Redirect to login
            return redirect('login')
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegisterForm()

    context = {
        'form': form,
        'page_title': 'Crear Cuenta',
    }
    return render(request, 'auth/register.html', context)


@require_http_methods(["POST"])
def logout_view(request):
    """
    Logout view - terminates user session.
    """
    logout(request)
    messages.success(request, '¡Hasta luego! Has cerrado sesión.')
    return redirect('login')


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


class ProfileUpdateForm(django_forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone', 'bio', 'profile_photo', 'cedula']
        widgets = {
            'bio': django_forms.Textarea(attrs={'rows': 3}),
        }


@login_required
@require_http_methods(["GET", "POST"])
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'profile/profile.html', {'form': form})


@login_required
def events_json(request):
    from administrative.models import StudentProfile

    user = request.user
    start_str = request.GET.get('start')
    end_str   = request.GET.get('end')

    if user.role == 'padre':
        hijos = StudentProfile.objects.filter(parent=user).values_list('user', flat=True)
        qs = ScheduleEvent.objects.filter(
            db_models.Q(attendees__in=hijos) | db_models.Q(created_by__in=hijos)
        ).distinct()
    else:
        qs = ScheduleEvent.objects.filter(
            db_models.Q(attendees=user) | db_models.Q(created_by=user)
        ).distinct()

    if start_str:
        qs = qs.filter(end__gte=parse_datetime(start_str))
    if end_str:
        qs = qs.filter(start__lte=parse_datetime(end_str))

    events = [
        {
            'id':    e.id,
            'title': e.title,
            'start': e.start.isoformat(),
            'end':   e.end.isoformat(),
            'allDay': e.all_day,
            'color': e.color,
            'url':   e.url or f'/eventos/{e.id}/',
            'extendedProps': {
                'type':        e.event_type,
                'description': e.description,
            },
        }
        for e in qs
    ]
    return JsonResponse(events, safe=False)


@login_required
def event_detail(request, event_id):
    event = get_object_or_404(ScheduleEvent, id=event_id)
    return render(request, 'calendar/event_detail.html', {'event': event})


@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user
    is_teacher = (course.teacher == user)
    is_enrolled = Enrollment.objects.filter(course=course, student=user, status='active').exists()

    if not is_teacher and not is_enrolled:
        return HttpResponseForbidden()

    qs = course.topics.all() if is_teacher else course.topics.filter(is_published=True)
    topics = qs.prefetch_related('materials')
    return render(request, 'academic/course_detail.html', {
        'course': course,
        'topics': topics,
        'is_teacher': is_teacher,
    })


class MaterialForm(django_forms.ModelForm):
    class Meta:
        model = TopicMaterial
        fields = ['title', 'material_type', 'file', 'url']
        widgets = {
            'url': django_forms.URLInput(attrs={'placeholder': 'https://...'}),
        }


@login_required
def material_upload(request, topic_id):
    topic = get_object_or_404(Topic.objects.select_related('course', 'course__teacher'), id=topic_id)
    if topic.course.teacher != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            mat = form.save(commit=False)
            mat.topic = topic
            mat.save()
            return redirect('topic-detail', topic_id=topic.id)
    else:
        form = MaterialForm()

    return render(request, 'academic/material_upload.html', {
        'form': form, 'topic': topic,
    })


class TopicForm(django_forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'description', 'order', 'date', 'is_published']
        widgets = {
            'description': django_forms.Textarea(attrs={'rows': 4}),
            'date': django_forms.DateInput(attrs={'type': 'date'}),
        }


@login_required
def topic_create(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.teacher != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.course = course
            topic.save()
            return redirect('course-detail', course_id=course.id)
    else:
        form = TopicForm()

    return render(request, 'academic/topic_form.html', {
        'form': form, 'course': course, 'action': 'Crear tema',
    })


@login_required
def topic_edit(request, topic_id):
    topic = get_object_or_404(Topic.objects.select_related('course', 'course__teacher'), id=topic_id)
    if topic.course.teacher != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('topic-detail', topic_id=topic.id)
    else:
        form = TopicForm(instance=topic)

    return render(request, 'academic/topic_form.html', {
        'form': form, 'course': topic.course, 'topic': topic, 'action': 'Editar tema',
    })


@login_required
def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic.objects.select_related('course', 'course__teacher'), id=topic_id)
    course = topic.course
    user = request.user
    is_teacher = (course.teacher == user)
    is_enrolled = Enrollment.objects.filter(course=course, student=user, status='active').exists()

    if not is_teacher and not is_enrolled:
        return HttpResponseForbidden()
    if not is_teacher and not topic.is_published:
        return HttpResponseForbidden()

    return render(request, 'academic/topic_detail.html', {
        'topic': topic,
        'course': course,
        'materials': topic.materials.all(),
        'is_teacher': is_teacher,
    })


import datetime

ATTENDANCE_STATUSES = [
    ('present', 'Presente'),
    ('absent', 'Ausente'),
    ('late', 'Tarde'),
    ('excused', 'Excusado'),
]

EVALUATION_TYPES = [
    ('exam', 'Examen'),
    ('quiz', 'Quiz'),
    ('assignment', 'Tarea'),
    ('project', 'Proyecto'),
    ('participation', 'Participación'),
    ('other', 'Otro'),
]


@login_required
def grade_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.teacher != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        eval_name = request.POST.get('evaluation_name', '').strip()
        eval_type = request.POST.get('evaluation_type', 'exam')
        max_score = request.POST.get('max_score', '100')
        weight = request.POST.get('weight', '1')
        if eval_name:
            import urllib.parse
            return redirect(
                f"/cursos/{course_id}/calificaciones/{urllib.parse.quote(eval_name, safe='')}/"
                f"?eval_type={eval_type}&max_score={max_score}&weight={weight}"
            )

    evaluations = (
        Grade.objects.filter(enrollment__course=course)
        .values('evaluation_name', 'evaluation_type', 'max_score', 'weight')
        .annotate(
            total=Count('id'),
            graded=Count('score', filter=Q(score__isnull=False)),
        )
        .order_by('evaluation_name')
    )

    return render(request, 'academic/grade_list.html', {
        'course': course,
        'evaluations': evaluations,
        'evaluation_types': EVALUATION_TYPES,
    })


@login_required
def grade_entry(request, course_id, evaluation_name):
    course = get_object_or_404(Course, id=course_id)
    if course.teacher != request.user:
        return HttpResponseForbidden()

    enrollments = (
        Enrollment.objects.filter(course=course, status='active')
        .select_related('student')
        .order_by('student__last_name', 'student__first_name')
    )

    existing = Grade.objects.filter(
        enrollment__course=course, evaluation_name=evaluation_name
    ).first()

    if existing:
        eval_type = existing.evaluation_type
        max_score = existing.max_score
        weight = existing.weight
    else:
        eval_type = request.GET.get('eval_type', 'exam')
        max_score = request.GET.get('max_score', '100')
        weight = request.GET.get('weight', '1')

    if request.method == 'POST':
        eval_type = request.POST.get('eval_type', eval_type)
        max_score_raw = request.POST.get('max_score', str(max_score))
        weight_raw = request.POST.get('weight', str(weight))

        for enrollment in enrollments:
            raw_score = request.POST.get(f'score_{enrollment.id}', '').strip()
            notes = request.POST.get(f'notes_{enrollment.id}', '').strip()
            score = None
            if raw_score != '':
                try:
                    score = float(raw_score)
                except ValueError:
                    pass
            Grade.objects.update_or_create(
                enrollment=enrollment,
                evaluation_name=evaluation_name,
                defaults={
                    'evaluation_type': eval_type,
                    'max_score': max_score_raw,
                    'weight': weight_raw,
                    'score': score,
                    'notes': notes,
                },
            )

        messages.success(request, f'Calificaciones guardadas para "{evaluation_name}".')
        return redirect('grade-list', course_id=course_id)

    grade_map = {
        g.enrollment_id: g
        for g in Grade.objects.filter(
            enrollment__course=course, evaluation_name=evaluation_name
        )
    }
    rows = [{'enrollment': e, 'grade': grade_map.get(e.id)} for e in enrollments]

    return render(request, 'academic/grade_entry.html', {
        'course': course,
        'evaluation_name': evaluation_name,
        'eval_type': eval_type,
        'max_score': max_score,
        'weight': weight,
        'rows': rows,
        'evaluation_types': EVALUATION_TYPES,
    })


@login_required
def attendance_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.teacher != request.user:
        return HttpResponseForbidden()

    dates = (
        Attendance.objects.filter(enrollment__course=course)
        .values('date')
        .annotate(
            present=Count('id', filter=Q(status='present')),
            absent=Count('id', filter=Q(status='absent')),
            late=Count('id', filter=Q(status='late')),
            excused=Count('id', filter=Q(status='excused')),
            total=Count('id'),
        )
        .order_by('-date')
    )

    today = datetime.date.today().isoformat()
    return render(request, 'academic/attendance_list.html', {
        'course': course,
        'dates': dates,
        'today': today,
    })


@login_required
def attendance_entry(request, course_id, date_str):
    course = get_object_or_404(Course, id=course_id)
    if course.teacher != request.user:
        return HttpResponseForbidden()

    try:
        entry_date = datetime.date.fromisoformat(date_str)
    except ValueError:
        return redirect('attendance-list', course_id=course_id)

    enrollments = (
        Enrollment.objects.filter(course=course, status='active')
        .select_related('student')
        .order_by('student__last_name', 'student__first_name')
    )

    if request.method == 'POST':
        for enrollment in enrollments:
            status = request.POST.get(f'status_{enrollment.id}', 'present')
            notes = request.POST.get(f'notes_{enrollment.id}', '').strip()
            Attendance.objects.update_or_create(
                enrollment=enrollment,
                date=entry_date,
                defaults={
                    'status': status,
                    'notes': notes,
                    'recorded_by': request.user,
                },
            )
        messages.success(request, f'Asistencia guardada para {entry_date.strftime("%d/%m/%Y")}.')
        return redirect('attendance-list', course_id=course_id)

    record_map = {
        a.enrollment_id: a
        for a in Attendance.objects.filter(
            enrollment__course=course, date=entry_date
        )
    }
    rows = [{'enrollment': e, 'record': record_map.get(e.id)} for e in enrollments]

    return render(request, 'academic/attendance_entry.html', {
        'course': course,
        'entry_date': entry_date,
        'rows': rows,
        'statuses': ATTENDANCE_STATUSES,
    })


EVENT_COLORS = {
    'class':        '#3b82f6',
    'evaluation':   '#ef4444',
    'task':         '#f59e0b',
    'meeting':      '#8b5cf6',
    'holiday':      '#10b981',
    'announcement': '#6b7280',
}

CREATOR_ROLES = {'admin', 'director', 'docente'}


@login_required
@require_http_methods(["POST"])
def event_create(request):
    if request.user.role not in CREATOR_ROLES:
        return JsonResponse({'error': 'Sin permiso'}, status=403)

    import json as _json
    try:
        data = _json.loads(request.body)
    except ValueError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    title = data.get('title', '').strip()
    if not title:
        return JsonResponse({'error': 'El título es requerido'}, status=400)

    event_type = data.get('event_type', 'class')
    all_day = bool(data.get('all_day', False))

    try:
        start = datetime.datetime.fromisoformat(data['start'])
        end = datetime.datetime.fromisoformat(data['end'])
    except (KeyError, ValueError):
        return JsonResponse({'error': 'Fechas inválidas'}, status=400)

    institution = getattr(request.user, 'institution', None)

    event = ScheduleEvent.objects.create(
        created_by=request.user,
        institution=institution,
        event_type=event_type,
        title=title,
        description=data.get('description', ''),
        study_material=data.get('study_material', ''),
        start=start,
        end=end,
        all_day=all_day,
        color=EVENT_COLORS.get(event_type, '#3b82f6'),
    )

    return JsonResponse({
        'id':    event.id,
        'title': event.title,
        'start': event.start.isoformat(),
        'end':   event.end.isoformat(),
        'allDay': event.all_day,
        'color': event.color,
        'url':   f'/eventos/{event.id}/',
        'extendedProps': {
            'type':          event.event_type,
            'description':   event.description,
            'study_material': event.study_material,
        },
    }, status=201)


@login_required
@require_http_methods(["POST"])
def mark_all_read(request):
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True, read_at=now)
    return JsonResponse({'ok': True})


def health_check(request):
    return JsonResponse({'status': 'ok'})
