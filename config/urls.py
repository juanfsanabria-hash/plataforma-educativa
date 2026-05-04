"""
URL configuration for config project.
API endpoints for Plataforma Educativa
"""
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

    # Event detail view
    path('eventos/<int:event_id>/', event_detail, name='event-detail'),

    # Course detail view
    path('cursos/<int:course_id>/', course_detail, name='course-detail'),

    # Topic detail view
    path('temas/<int:topic_id>/', topic_detail, name='topic-detail'),

    # REST API endpoints
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/', include('rest_framework.urls')),
    path('api-token-auth/', authtoken_views.obtain_auth_token, name='api-token-auth'),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
