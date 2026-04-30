from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomUser


class LoginForm(forms.Form):
    """Formulario de login con email y contraseña."""

    email = forms.EmailField(
        label=_('Correo Electrónico'),
        max_length=255,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'tu@email.com',
            'autocomplete': 'email',
        })
    )

    password = forms.CharField(
        label=_('Contraseña'),
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': '••••••••',
            'autocomplete': 'current-password',
        })
    )

    remember_me = forms.BooleanField(
        label=_('Recuérdame'),
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-2 focus:ring-blue-500',
        })
    )

    def clean(self):
        """Validar credenciales de login."""
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            # Intentar autenticar con email como username
            try:
                user = CustomUser.objects.get(email=email)
                self.user = authenticate(username=user.username, password=password)
                if self.user is None:
                    raise ValidationError(
                        _('Email o contraseña inválidos.'),
                        code='invalid_credentials',
                    )
            except CustomUser.DoesNotExist:
                raise ValidationError(
                    _('Email o contraseña inválidos.'),
                    code='user_not_found',
                )

        return cleaned_data

    def get_user(self):
        """Retorna el usuario autenticado."""
        return getattr(self, 'user', None)


class RegisterForm(UserCreationForm):
    """Formulario de registro con validación completa."""

    first_name = forms.CharField(
        label=_('Nombre'),
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Tu nombre',
            'autocomplete': 'given-name',
        })
    )

    last_name = forms.CharField(
        label=_('Apellido'),
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Tu apellido',
            'autocomplete': 'family-name',
        })
    )

    email = forms.EmailField(
        label=_('Correo Electrónico'),
        max_length=255,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'tu@email.com',
            'autocomplete': 'email',
        })
    )

    cedula = forms.CharField(
        label=_('Cédula / Identificación'),
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': '1234567890',
            'autocomplete': 'off',
        })
    )

    role = forms.ChoiceField(
        label=_('Rol en la Plataforma'),
        choices=[
            ('', '-- Selecciona un rol --'),
            ('estudiante', _('Estudiante')),
            ('padre', _('Padre/Madre/Acudiente')),
            ('docente', _('Docente')),
            ('director', _('Director/Directora')),
        ],
        required=True,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        })
    )

    password1 = forms.CharField(
        label=_('Contraseña'),
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': '••••••••',
            'autocomplete': 'new-password',
        }),
        help_text=_('Mínimo 8 caracteres, debe incluir letras y números'),
    )

    password2 = forms.CharField(
        label=_('Confirma tu Contraseña'),
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': '••••••••',
            'autocomplete': 'new-password',
        })
    )

    agree_terms = forms.BooleanField(
        label=_('Acepto los términos y condiciones'),
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-2 focus:ring-blue-500',
        })
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'cedula', 'role', 'password1', 'password2')

    def clean_email(self):
        """Validar que el email sea único."""
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError(
                _('Este correo ya está registrado. ¿Deseas iniciar sesión?'),
                code='email_exists',
            )
        return email

    def clean_cedula(self):
        """Validar que la cédula sea única si se proporciona."""
        cedula = self.cleaned_data.get('cedula')
        if cedula and CustomUser.objects.filter(cedula=cedula).exists():
            raise ValidationError(
                _('Esta cédula ya está registrada.'),
                code='cedula_exists',
            )
        return cedula

    def clean_password1(self):
        """Validar fortaleza de contraseña."""
        password1 = self.cleaned_data.get('password1')

        if password1:
            # Mínimo 8 caracteres
            if len(password1) < 8:
                raise ValidationError(
                    _('La contraseña debe tener al menos 8 caracteres.'),
                    code='password_too_short',
                )

            # Debe contener al menos una letra y un número
            has_letter = any(c.isalpha() for c in password1)
            has_digit = any(c.isdigit() for c in password1)

            if not (has_letter and has_digit):
                raise ValidationError(
                    _('La contraseña debe contener letras y números.'),
                    code='password_weak',
                )

        return password1

    def clean_password2(self):
        """Validar que las contraseñas coincidan."""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    _('Las contraseñas no coinciden.'),
                    code='password_mismatch',
                )

        return password2

    def clean_role(self):
        """Validar que se seleccione un rol válido."""
        role = self.cleaned_data.get('role')
        if not role:
            raise ValidationError(
                _('Debes seleccionar un rol.'),
                code='invalid_role',
            )
        return role

    def clean_agree_terms(self):
        """Validar que acepte los términos."""
        agree_terms = self.cleaned_data.get('agree_terms')
        if not agree_terms:
            raise ValidationError(
                _('Debes aceptar los términos y condiciones.'),
                code='terms_not_accepted',
            )
        return agree_terms

    def save(self, commit=True):
        """Guardar usuario con email como username."""
        user = super().save(commit=False)

        # Usar email como username
        user.username = self.cleaned_data['email']

        if commit:
            user.save()

        return user
