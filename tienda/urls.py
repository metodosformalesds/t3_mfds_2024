from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Página de inicio y productos
    path('', views.index, name='index'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('producto/<str:id>/', views.detalle_producto, name='detalle_producto'),
    path('carrito/', views.carrito, name='carrito'),
    path('agregar-al-carrito/<str:id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('vaciar-carrito/', views.vaciar_carrito, name='vaciar_carrito'),
    path('checkout/', views.checkout, name='checkout'),
    path('historial/', views.historial_pedidos, name='historial'),

    # Nueva ruta para detalles del yonke
    path('yonke/<str:place_id>/', views.detalle_yonke, name='detalle_yonke'),

    # Account and authentication paths
    path('accounts/', views.account_view, name='account'),  # Vista personalizada de cuentas para escoger cliente o yonkero
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    # Django Allauth urls para autenticación social y administración de cuentas
    path('social/', include('allauth.urls')),  # Nota: Cambié el prefijo para evitar conflicto con 'accounts/'

    # Custom login and signup paths for diferentes tipos de usuario
    path('user/login/', views.user_login, name='user_login'),  # Página de login para usuarios normales
    path('user/signup/', views.user_signup, name='user_signup'),  # Página de registro para usuarios normales
    path('yonkero/login/', views.yonkero_login, name='yonkero_login'),  # Página de login para yonkeros
    path('yonkero/signup/', views.yonkero_signup, name='yonkero_signup'),  # Página de registro para yonkeros
]
