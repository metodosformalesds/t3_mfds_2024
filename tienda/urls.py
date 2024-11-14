from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('producto/<str:id>/', views.detalle_producto, name='detalle_producto'),
    path('carrito/', views.carrito, name='carrito'),
    path('agregar-al-carrito/<str:id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('vaciar-carrito/', views.vaciar_carrito, name='vaciar_carrito'),
    path('checkout/', views.checkout, name='checkout'),
    path('historial/', views.historial_pedidos, name='historial'),

    # Account and authentication paths
    path('accounts/', views.account_view, name='account'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('accounts/', include('allauth.urls')),
]
