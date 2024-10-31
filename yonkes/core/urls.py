from django.urls import path
from .views import complete_profile, home

urlpatterns = [
    path('', home, name='home'),
    path('completar-perfil/', complete_profile, name='complete_profile'),
]