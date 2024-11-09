from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Producto, ImagenProducto, CartItem
from .forms import CompleteProfileForm, ProductoForm
from django.db.models import ExpressionWrapper, F, DurationField
from django.utils.timezone import now
from django.http import JsonResponse
import json

# Vista para la página Home con lógica de autenticación
def home(request):
    user_name = None
    if request.user.is_authenticated:
        user_name = request.user.get_full_name() or request.user.username

    return render(request, 'home.html', {'user_name': user_name})

@login_required
def complete_profile(request):
    user = request.user

    # Verifica si el perfil del usuario está completo
    if user.street and user.city and user.role:
        # Si el perfil está completo, redirige al panel correspondiente
        if user.role == 'vendedor':
            return redirect('vendedor_panel_url')
        elif user.role == 'comprador':
            return redirect('comprador_panel')
    
    # Si el perfil no está completo, muestra el formulario para completarlo
    if request.method == 'POST':
        form = CompleteProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # Una vez completado el perfil, redirige al panel correspondiente
            if user.role == 'vendedor':
                return redirect('vendedor_panel_url')
            elif user.role == 'comprador':
                return redirect('comprador_panel')
    else:
        form = CompleteProfileForm(instance=user)

    return render(request, 'core/complete_profile.html', {'form': form})

# Panel de vendedor
@login_required
def vendedor_panel(request):
    productos = Producto.objects.filter(vendedor=request.user)
    return render(request, 'core/vendedor_panel.html', {'productos': productos})

# Panel de comprador
@login_required
def comprador_panel(request):
    return render(request, 'core/comprador_panel.html')

# Nueva vista: Redirección después de iniciar sesión
@login_required
def redirect_after_login(request):
    user = request.user
    # Si el perfil no está completo, redirige a completar el perfil
    if not (user.street and user.city and user.role):
        return redirect('complete_profile_url')
    elif user.role == 'vendedor':
        return redirect('vendedor_panel_url')
    elif user.role == 'comprador':
        return redirect('comprador_panel')
    else:
        return redirect('/')  # O maneja el caso de redirección por defecto si algo sale mal

from datetime import timedelta
#PRODUCTOS
@login_required
def listar_productos(request):
    # Utilizamos la misma lógica de verificación de orden
    productos = Producto.objects.filter(vendedor=request.user).order_by('-created_at')
    return render(request, 'core/verificar_orden.html', {'productos': productos})

#pendienteeeee
@login_required
def verificar_orden_productos(request):
    productos = Producto.objects.filter(vendedor=request.user).order_by('-created_at')
    return render(request, 'core/verificar_orden.html', {'productos': productos})

@login_required
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'core/detalle_producto.html', {'producto': producto})

@login_required
def producto_detalle_comprador(request, id):
    # Obtener el producto específico, solo si su estatus es 'disponible'
    producto = get_object_or_404(Producto, id=id, estatus='disponible')
    return render(request, 'core/producto_detalle_comprador.html', {'producto': producto})




@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        archivos = request.FILES.getlist('imagenes')  # Asegúrate de que se obtengan los archivos
        if form.is_valid():
            producto = form.save(commit=False)
            producto.vendedor = request.user
            producto.save()

            # Guardar cada imagen en el modelo ImagenProducto
            for archivo in archivos:
                ImagenProducto.objects.create(producto=producto, imagen=archivo)

            return redirect('vendedor_panel_url')  # Asegúrate de que 'vendedor_panel_url' sea correcto
    else:
        form = ProductoForm()
    return render(request, 'core/agregar_producto.html', {'form': form})

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk, vendedor=request.user)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            # Redirige al Panel del Vendedor después de guardar en lugar de la lista de productos
            return redirect('vendedor_panel_url')  # Asegúrate de que 'vendedor_panel_url' es el nombre correcto de la URL del panel
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'core/editar_producto.html', {'form': form})

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk, vendedor=request.user)
    if request.method == 'POST':
        producto.delete()
        # Redirige al panel de vendedor después de eliminar
        return redirect('vendedor_panel_url')  # Asegúrate de que 'vendedor_panel_url' sea el nombre correcto
    
# panel de comprador
def comprador_panel(request):
    # Obtener la categoría seleccionada del formulario
    categoria_seleccionada = request.GET.get('category', 'Todas')

    # Filtrar los productos disponibles según la categoría seleccionada
    if categoria_seleccionada and categoria_seleccionada != 'Todas':
        productos = Producto.objects.filter(categoria=categoria_seleccionada, estatus='disponible')
    else:
        productos = Producto.objects.filter(estatus='disponible')

    # Obtener todas las categorías para mostrar en el formulario de filtro
    categorias = Producto.objects.filter(estatus='disponible').values_list('categoria', flat=True).distinct()

    return render(request, 'core/comprador_panel.html', {
        'productos': productos,
        'categorias': categorias,
        'selected_category': categoria_seleccionada
    })

#carrito
def ver_carrito(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.subtotal() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'core/carrito.html', context)

def actualizar_carrito(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        nueva_cantidad = int(request.POST.get('quantity', 1))
        cart_item.quantity = nueva_cantidad
        cart_item.save()
    return redirect('ver_carrito')

def eliminar_del_carrito(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('ver_carrito')

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, producto=producto)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('ver_carrito')