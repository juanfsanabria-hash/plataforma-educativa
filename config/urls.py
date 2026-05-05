"""
URL configuration for config project.
API endpoints for Plataforma Educativa
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from accounts.admin import secure_admin
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as authtoken_views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from accounts.views import CustomUserViewSet, InstitutionViewSet, AcademicYearViewSet
from academic.views import CourseViewSet, EnrollmentViewSet, GradeViewSet, AttendanceViewSet
from administrative.views import StudentProfileViewSet, PaymentViewSet
from communication.views import AnnouncementViewSet, MessageViewSet, NotificationViewSet
from core.views import (
    home,
    login_view,
    register_view,
    logout_view,
    admin_dashboard,
    director_dashboard,
    docente_dashboard,
    estudiante_dashboard,
    padre_dashboard,
    health_check,
    profile_view,
    events_json,
    event_detail,
    course_detail,
    topic_detail,
    topic_create,
    topic_edit,
    material_upload,
    grade_list,
    grade_entry,
    attendance_list,
    attendance_entry,
    event_create,
    mark_all_read,
    student_grades,
    student_attendance,
    parent_child_grades,
    parent_child_attendance,
    announcement_list,
    announcement_create,
    announcement_detail,
)

# API Router
router = DefaultRouter()

# Accounts endpoints
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'institutions', InstitutionViewSet, basename='institution')
router.register(r'academic-years', AcademicYearViewSet, basename='academic-year')

# Academic endpoints
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'grades', GradeViewSet, basename='grade')
router.register(r'attendance', AttendanceViewSet, basename='attendance')

# Administrative endpoints
router.register(r'student-profiles', StudentProfileViewSet, basename='student-profile')
router.register(r'payments', PaymentViewSet, basename='payment')

# Communication endpoints
router.register(r'announcements', AnnouncementViewSet, basename='announcement')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    # Health check (no auth, no DB)
    path('health/', health_check, name='health-check'),

    # Authentication views (HTML)
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('perfil/', profile_view, name='profile'),

    # Dashboard views (HTML)
    path('', home, name='home'),
    path('dashboard/admin/', admin_dashboard, name='admin-dashboard'),
    path('dashboard/director/', director_dashboard, name='director-dashboard'),
    path('dashboard/docente/', docente_dashboard, name='docente-dashboard'),
    path('dashboard/estudiante/', estudiante_dashboard, name='estudiante-dashboard'),
    path('dashboard/padre/', padre_dashboard, name='padre-dashboard'),

    # Admin interface
    path('admin/', secure_admin.urls),

    # FullCalendar JSON feed
    path('api/events/', events_json, name='events-json'),

    # Event create endpoint (POST JSON)
    path('api/eventos/crear/', event_create, name='event-create'),

    # Notifications
    path('api/notificaciones/marcar-todas/', mark_all_read, name='mark-all-read'),

    # Student consolidated views
    path('mis-notas/', student_grades, name='student-grades'),
    path('mi-asistencia/', student_attendance, name='student-attendance'),

    # Parent child views
    path('mis-hijos/<int:student_id>/notas/', parent_child_grades, name='parent-child-grades'),
    path('mis-hijos/<int:student_id>/asistencia/', parent_child_attendance, name='parent-child-attendance'),

    # Announcements
    path('anuncios/', announcement_list, name='announcement-list'),
    path('anuncios/nuevo/', announcement_create, name='announcement-create'),
    path('anuncios/<int:pk>/', announcement_detail, name='announcement-detail'),

    # Event detail view
    path('eventos/<int:event_id>/', event_detail, name='event-detail'),

    # Course detail view
    path('cursos/<int:course_id>/', course_detail, name='course-detail'),

    # Topic detail view
    path('temas/<int:topic_id>/', topic_detail, name='topic-detail'),

    # Topic create/edit views
    path('cursos/<int:course_id>/temas/nuevo/', topic_create, name='topic-create'),
    path('temas/<int:topic_id>/editar/', topic_edit, name='topic-edit'),

    # Material upload view
    path('temas/<int:topic_id>/materiales/subir/', material_upload, name='material-upload'),

    # Grade management views
    path('cursos/<int:course_id>/calificaciones/', grade_list, name='grade-list'),
    path('cursos/<int:course_id>/calificaciones/<str:evaluation_name>/', grade_entry, name='grade-entry'),

    # Attendance management views
    path('cursos/<int:course_id>/asistencia/', attendance_list, name='attendance-list'),
    path('cursos/<int:course_id>/asistencia/<str:date_str>/', attendance_entry, name='attendance-entry'),

    # REST API endpoints
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/', include('rest_framework.urls')),
    path('api-token-auth/', authtoken_views.obtain_auth_token, name='api-token-auth'),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
