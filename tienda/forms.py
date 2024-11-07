from django import forms
from django.contrib.auth.models import User
from .models import PerfilUsuario, Producto
from allauth.account.forms import LoginForm, SignupForm

# Formulario para manejar la creación y edición de productos
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'imagen']

# Formulario de registro personalizado para usuarios estándar
class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    rol = forms.ChoiceField(choices=PerfilUsuario.ROLES)

    class Meta:
        model = User
        fields = ['username', 'password']

# Formulario para gestionar el perfil de usuario (roles)
class PerfilForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['rol']

# Formulario personalizado de inicio de sesión utilizando Allauth
class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({
            'placeholder': 'Correo electrónico o nombre de usuario',
            'class': 'input-box'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Contraseña',
            'class': 'input-box'
        })

# Formulario personalizado de registro utilizando Allauth
class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Nombre de usuario',
            'class': 'input-box'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Correo electrónico',
            'class': 'input-box'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Contraseña',
            'class': 'input-box'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirmar contraseña',
            'class': 'input-box'
        })

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        # Aquí puedes agregar lógica adicional si necesitas, por ejemplo, crear un PerfilUsuario.
        PerfilUsuario.objects.create(user=user, rol='comprador')  # Rol predeterminado: comprador.
        return user
