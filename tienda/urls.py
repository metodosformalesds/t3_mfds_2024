# tienda/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo, name='catalogo'),  # Catálogo de productos
    path('producto/<int:id>/', views.detalle_producto, name='detalle_producto'),  # Detalle del producto
    path('carrito/', views.carrito, name='carrito'),  # Vista del carrito
    path('agregar/<int:id>/', views.agregar_al_carrito, name='agregar_al_carrito'),  # Agregar al carrito
    path('vaciar-carrito/', views.vaciar_carrito, name='vaciar_carrito'),  # Vaciar carrito
    path('checkout/', views.checkout, name='checkout'),  # Ruta para el checkout
    path('historial/', views.historial_pedidos, name='historial'),  # Nueva ruta para historial

]

