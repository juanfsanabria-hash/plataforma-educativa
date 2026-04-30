from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Course, Enrollment, Grade, Attendance
from .serializers import CourseSerializer, EnrollmentSerializer, GradeSerializer, AttendanceSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """API endpoints for courses"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['institution', 'academic_year', 'teacher', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']


class EnrollmentViewSet(viewsets.ModelViewSet):
    """API endpoints for enrollments"""
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['course', 'student', 'status']
    search_fields = ['student__email', 'course__name']


class GradeViewSet(viewsets.ModelViewSet):
    """API endpoints for grades"""
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['enrollment', 'evaluation_type']
    search_fields = ['evaluation_name']
    ordering_fields = ['recorded_date', 'score']


class AttendanceViewSet(viewsets.ModelViewSet):
    """API endpoints for attendance"""
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['enrollment', 'status', 'date']
    search_fields = ['enrollment__student__email']
    ordering_fields = ['date']
