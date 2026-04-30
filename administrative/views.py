from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import StudentProfile, Payment
from .serializers import StudentProfileSerializer, PaymentSerializer


class StudentProfileViewSet(viewsets.ModelViewSet):
    """API endpoints for student profiles"""
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['institution', 'academic_year', 'enrollment_status']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']


class PaymentViewSet(viewsets.ModelViewSet):
    """API endpoints for payments"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['institution', 'status', 'due_date']
    search_fields = ['student_profile__user__email', 'concept']
    ordering_fields = ['due_date', 'amount']
