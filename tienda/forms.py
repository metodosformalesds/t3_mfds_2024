# forms.py (Ajustes menores para mejorar mensajes de error)

from django import forms
from django.contrib.auth.models import User
from .models import PerfilUsuario, Producto
from allauth.account.forms import LoginForm, SignupForm
from django.utils.translation import gettext_lazy as _

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={
            'placeholder': 'Correo electrónico o nombre de usuario',  # Permitir ambos
            'class': 'form-control'
        })
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'class': 'form-control'
        })
        
    def login(self, *args, **kwargs):
        try:
            return super(CustomLoginForm, self).login(*args, **kwargs)
        except forms.ValidationError as e:
            self.add_error(None, e)
            return None

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': _('Nombre de usuario'),
            'class': 'input-box',
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': _('Correo electrónico'),
            'class': 'input-box',
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': _('Contraseña'),
            'class': 'input-box',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': _('Confirmar contraseña'),
            'class': 'input-box',
        })

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_("Este nombre de usuario ya está en uso. Por favor, elige otro."))
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Este correo electrónico ya está registrado."))
        return email

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        PerfilUsuario.objects.create(user=user, rol='comprador')
        return user

from django import forms
from allauth.account.forms import SignupForm
from .models import PerfilUsuario, Yonke


class YonkeroSignupForm(SignupForm):
    username = forms.CharField(
        label="Nombre de Usuario",
        max_length=30,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nombre de Usuario',
            'class': 'input-box',
        }),
        required=True,
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'class': 'input-box',
        }),
        required=True,
    )
    password2 = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirmar Contraseña',
            'class': 'input-box',
        }),
        required=True,
    )
    junkyard_name = forms.CharField(
        label="Nombre del Yonke",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nombre del Yonke',
            'class': 'input-box',
        }),
    )
    junkyard_address = forms.CharField(
        label="Dirección del Yonke",
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Dirección del Yonke',
            'class': 'input-box',
        }),
    )

    def save(self, request):
        # Guardar el usuario utilizando la lógica base de SignupForm
        user = super().save(request)

        # Crear un perfil de usuario con rol de 'vendedor'
        PerfilUsuario.objects.create(usuario=user, rol='vendedor')

        # Guardar información del Yonke
        Yonke.objects.create(
            vendedor=user,
            nombre=self.cleaned_data['junkyard_name'],
            direccion=self.cleaned_data['junkyard_address'],
            latitud=0.0,  # Puedes configurar esto con geocodificación si es necesario
            longitud=0.0
        )

        return user
