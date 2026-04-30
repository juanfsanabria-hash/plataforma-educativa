from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, Institution, AcademicYear


class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser with full profile info"""

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'cedula',
                  'phone', 'profile_photo', 'bio', 'is_active', 'created_at')
        read_only_fields = ('id', 'created_at')


class CustomUserDetailSerializer(CustomUserSerializer):
    """Extended serializer with sensitive fields for own profile"""

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + ('username',)


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'cedula', 'password', 'password_confirm', 'role')

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden"})
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Este email ya está registrado"})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for login"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Credenciales inválidas")
        data['user'] = user
        return data


class InstitutionSerializer(serializers.ModelSerializer):
    """Serializer for Institution"""
    admin_users = CustomUserSerializer(many=True, read_only=True)

    class Meta:
        model = Institution
        fields = ('id', 'name', 'slug', 'description', 'logo', 'address',
                  'phone', 'email', 'website', 'admin_users', 'is_active', 'created_at')
        read_only_fields = ('id', 'created_at')


class AcademicYearSerializer(serializers.ModelSerializer):
    """Serializer for AcademicYear"""
    institution_name = serializers.CharField(source='institution.name', read_only=True)

    class Meta:
        model = AcademicYear
        fields = ('id', 'institution', 'institution_name', 'name', 'year',
                  'start_date', 'end_date', 'is_active', 'created_at')
        read_only_fields = ('id', 'created_at')
