from . import views
from django.contrib.auth import views as auth_views
from django.urls import path, include


urlpatterns = [
    path('', views.index, name='index'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('producto/<int:id>/', views.detalle_producto, name='detalle_producto'),
    path('carrito/', views.carrito, name='carrito'),
    path('agregar/<int:id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('vaciar_carrito/', views.vaciar_carrito, name='vaciar_carrito'),
    path('checkout/', views.checkout, name='checkout'),
    path('historial/', views.historial_pedidos, name='historial'),
    path('registro/', views.registro, name='registro'),
    path('publicar/', views.publicar_producto, name='publicar_producto'),  
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),  # Redirigir al índice
    path('accounts/', include('allauth.urls')),
    path('mapa/', views.mapa_ubicacion, name='mapa_ubicacion'),
    path('api/yonkes/', views.lista_yonkes, name='lista_yonkes'),



]


