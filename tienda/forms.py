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
