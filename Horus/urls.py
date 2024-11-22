from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from tienda import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tienda.urls')),  # URLs personalizadas de la aplicación 'tienda'

    # URLs relacionadas con el sistema de autenticación de 'django-allauth'
    path('accounts/', include('allauth.urls')),  # Incluyendo las URLs de allauth para registro e inicio de sesión

    # Stripe URLs
    path('stripe/checkout/', views.stripe_checkout, name='stripe_checkout'),
    path('stripe/success/', views.stripe_success, name='stripe_success'),
    path('stripe/cancel/', views.stripe_cancel, name='stripe_cancel'),

    # PayPal URLs
    path('paypal/checkout/', views.paypal_checkout, name='paypal_checkout'),
    path('paypal/success/', views.paypal_success, name='paypal_success'),
    path('paypal/cancel/', views.paypal_cancel, name='paypal_cancel'),
]

# Agregar configuración para archivos media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
