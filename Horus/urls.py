from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tienda.urls')),  # URLs personalizadas de la aplicación 'tienda'

    # URLs relacionadas con el sistema de autenticación de 'django-allauth'
    path('accounts/', include('allauth.urls')),  # Incluyendo las URLs de allauth para registro e inicio de sesión

    # Puedes agregar más URLs según sea necesario aquí
]

# Agregar configuración para archivos media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
