from django.urls import path
from . import views  # Asegúrate de que las vistas se importan correctamente

urlpatterns = [
    path('', views.home, name='home'),  # Ruta para la página de inicio
    path('completar-perfil/', views.complete_profile, name='complete_profile'),
    path('panel-vendedor/', views.vendedor_panel, name='vendedor_panel_url'),
    path('panel-comprador/', views.comprador_panel, name='comprador_panel'),
    path('redirect-after-login/', views.redirect_after_login, name='redirect_after_login'),  # Nueva ruta para la redirección
    path('completar-perfil/', views.complete_profile, name='complete_profile_url'),

    #productos
    path('productos/', views.listar_productos, name='listar_productos'),
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('verificar-orden/', views.verificar_orden_productos, name='verificar_orden_productos'),
    path('productos/detalles/<int:pk>/', views.detalle_producto, name='detalle_producto'),
    path('productos/detalle/<int:pk>/', views.detalle_producto, name='detalle_producto'),
    path('product/<int:id>/detalle_comprador/', views.producto_detalle_comprador, name='producto_detalle_comprador'),
    
    #carrito
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('ver_carrito/', views.ver_carrito, name='ver_carrito'),
    path('actualizar_carrito/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('eliminar_del_carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
]  