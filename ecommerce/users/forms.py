from django import forms
from allauth.account.forms import SignupForm
from .models import Profile

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=100, label='Nombre')
    last_name = forms.CharField(max_length=100, label='Apellido')
    profile_type = forms.ChoiceField(choices=Profile.USER_TYPES, label='Tipo de Perfil')
    address = forms.CharField(max_length=255, label='Dirección')
    photo_id = forms.ImageField(label='Credencial de Elector')

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        profile = Profile.objects.get(user=user)
        profile.profile_type = self.cleaned_data['profile_type']
        profile.address = self.cleaned_data['address']
        profile.photo_id = self.cleaned_data['photo_id']
        profile.save()

        return user
