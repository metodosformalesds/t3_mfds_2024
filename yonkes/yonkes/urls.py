from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),  # Redirigir al home
    path('accounts/', include('allauth.urls')),  # Solo usa allauth.urls
]
