from django import forms
from django.contrib.auth.models import User
from .models import PerfilUsuario
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'imagen']

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    rol = forms.ChoiceField(choices=PerfilUsuario.ROLES)

    class Meta:
        model = User
        fields = ['username', 'password']

class PerfilForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['rol']