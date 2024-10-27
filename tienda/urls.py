from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

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
    path('publicar/', views.publicar_producto, name='publicar_producto'),  # Ruta para publicar productos
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),  # Logout

]