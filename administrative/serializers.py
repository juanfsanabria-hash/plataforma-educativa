from rest_framework import serializers
from .models import StudentProfile, Payment


class StudentProfileSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='user.get_full_name', read_only=True)
    institution_name = serializers.CharField(source='institution.name', read_only=True)

    class Meta:
        model = StudentProfile
        fields = ('id', 'user', 'student_name', 'institution', 'institution_name',
                  'academic_year', 'date_of_birth', 'gender', 'address',
                  'emergency_contact', 'emergency_phone', 'parent_names',
                  'enrollment_status', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class PaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student_profile.user.get_full_name', read_only=True)
    institution_name = serializers.CharField(source='institution.name', read_only=True)

    class Meta:
        model = Payment
        fields = ('id', 'institution', 'institution_name', 'student_profile',
                  'student_name', 'concept', 'amount', 'currency', 'status',
                  'due_date', 'paid_date', 'payment_method', 'notes',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
