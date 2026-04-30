from rest_framework import serializers
from .models import Course, Enrollment, Grade, Attendance


class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'name', 'slug', 'institution', 'academic_year', 'teacher',
                  'teacher_name', 'description', 'credits', 'schedule_description',
                  'is_active', 'created_at')
        read_only_fields = ('id', 'created_at')


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = Enrollment
        fields = ('id', 'course', 'course_name', 'student', 'student_name',
                  'status', 'enrolled_date', 'created_at')
        read_only_fields = ('id', 'enrolled_date', 'created_at')


class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='enrollment.student.get_full_name', read_only=True)
    course_name = serializers.CharField(source='enrollment.course.name', read_only=True)

    class Meta:
        model = Grade
        fields = ('id', 'enrollment', 'student_name', 'course_name', 'evaluation_name',
                  'evaluation_type', 'score', 'max_score', 'weight', 'recorded_date', 'notes')
        read_only_fields = ('id', 'recorded_date')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['percentage'] = instance.percentage()
        return data


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='enrollment.student.get_full_name', read_only=True)
    recorded_by_name = serializers.CharField(source='recorded_by.get_full_name', read_only=True)

    class Meta:
        model = Attendance
        fields = ('id', 'enrollment', 'student_name', 'date', 'status',
                  'recorded_by', 'recorded_by_name', 'notes', 'created_at')
        read_only_fields = ('id', 'created_at')
