from django import forms
from allauth.account.forms import SignupForm
from .models import CustomUser

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label="Nombre")
    last_name = forms.CharField(max_length=30, label="Apellido")
    age = forms.IntegerField(min_value=18, label="Edad")  # Validación de edad
    address = forms.CharField(max_length=255, label="Dirección")
    phone_number = forms.CharField(max_length=15, label="Número de teléfono")
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, label="Rol")

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.age = self.cleaned_data.get('age')
        user.address = self.cleaned_data.get('address')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.role = self.cleaned_data.get('role')
        user.is_profile_complete = True
        user.save()
        return user
