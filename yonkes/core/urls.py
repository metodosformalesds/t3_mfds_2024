from django.urls import path
from . import views  # Asegúrate de que las vistas se importan correctamente

urlpatterns = [
    path('', views.home, name='home'),  # Ruta para la página de inicio
    path('completar-perfil/', views.complete_profile, name='complete_profile'),
    path('panel-vendedor/', views.vendedor_panel, name='vendedor_panel_url'),
    path('panel-comprador/', views.comprador_panel, name='comprador_panel_url'),
    path('redirect-after-login/', views.redirect_after_login, name='redirect_after_login'),  # Nueva ruta para la redirección
    path('completar-perfil/', views.complete_profile, name='complete_profile_url'),

    #productos
    path('productos/', views.listar_productos, name='listar_productos'),
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('verificar-orden/', views.verificar_orden_productos, name='verificar_orden_productos'),
    path('productos/detalle/<int:pk>/', views.detalle_producto, name='detalle_producto'),
]  