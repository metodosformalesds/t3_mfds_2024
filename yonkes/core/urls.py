from django.urls import path
from . import views  # Asegúrate de que las vistas se importan correctamente

urlpatterns = [
    path('', views.home, name='home'),  # Ruta para la página de inicio
    path('completar-perfil/', views.complete_profile, name='complete_profile'),
    path('panel-vendedor/', views.vendedor_panel, name='vendedor_panel_url'),
    path('panel-comprador/', views.comprador_panel, name='comprador_panel_url'),
    path('redirect-after-login/', views.redirect_after_login, name='redirect_after_login'),  # Nueva ruta para la redirección
]