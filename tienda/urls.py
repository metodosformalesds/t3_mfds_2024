from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Página de inicio, usando la plantilla actualizada 'index.html'
    path('', views.index, name='index'),

    # Catálogo de productos (usando la plantilla actualizada 'products.html')
    path('catalogo/', views.catalogo, name='catalogo'),

    # Detalles del producto específico por su ID (usando 'product_details.html')
    path('producto/<str:id>/', views.detalle_producto, name='detalle_producto'),

    # Carrito de compras
    path('carrito/', views.carrito, name='carrito'),

    # Añadir producto al carrito de compras por su ID
    path('agregar-al-carrito/<str:id>/', views.agregar_al_carrito, name='agregar_al_carrito'),

    # Vaciar el carrito de compras
    path('vaciar-carrito/', views.vaciar_carrito, name='vaciar_carrito'),

    # Proceso de pago (checkout)
    path('checkout/', views.checkout, name='checkout'),

    # Historial de pedidos del usuario
    path('historial/', views.historial_pedidos, name='historial'),

    # Registro de usuario nuevo (redirigir a la vista 'account_view')
    path('registro/', views.account_view, name='registro'),

    # Publicar un nuevo producto por el vendedor
    path('publicar/', views.publicar_producto, name='publicar_producto'),

    # Vista para iniciar sesión (usando la plantilla 'registration/login.html')
    path('login/', auth_views.LoginView.as_view(template_name='account.html'), name='login'),

    # Vista para cerrar sesión y redirigir al índice
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    # URLs relacionadas con el sistema de autenticación de 'django-allauth'
    path('accounts/', include('allauth.urls')),
]
