"""
URL configuration for config project.
API endpoints for Plataforma Educativa
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as authtoken_views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from accounts.views import CustomUserViewSet, InstitutionViewSet, AcademicYearViewSet
from academic.views import CourseViewSet, EnrollmentViewSet, GradeViewSet, AttendanceViewSet
from administrative.views import StudentProfileViewSet, PaymentViewSet
from communication.views import AnnouncementViewSet, MessageViewSet, NotificationViewSet
from core.views import (
    home,
    admin_dashboard,
    director_dashboard,
    docente_dashboard,
    estudiante_dashboard,
    padre_dashboard,
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
    # Dashboard views (HTML)
    path('', home, name='home'),
    path('dashboard/admin/', admin_dashboard, name='admin-dashboard'),
    path('dashboard/director/', director_dashboard, name='director-dashboard'),
    path('dashboard/docente/', docente_dashboard, name='docente-dashboard'),
    path('dashboard/estudiante/', estudiante_dashboard, name='estudiante-dashboard'),
    path('dashboard/padre/', padre_dashboard, name='padre-dashboard'),

    # Admin interface
    path('admin/', admin.site.urls),

    # REST API endpoints
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/', include('rest_framework.urls')),
    path('api-token-auth/', authtoken_views.obtain_auth_token, name='api-token-auth'),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
