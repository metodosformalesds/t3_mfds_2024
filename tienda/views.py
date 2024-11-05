# tienda/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Orden, DetalleOrden, Categoria
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import ProductoForm
from django.http import JsonResponse

def index(request):
    # Obtener todas las categorías desde la base de datos para mostrarlas en el index
    categorias = Categoria.objects.all()
    return render(request, 'index.html', {'categorias': categorias})

def account_view(request):
    # Vista unificada para el inicio de sesión y registro
    return render(request, 'account.html')

@login_required
def publicar_producto(request):
    # Verificar que el usuario sea un vendedor antes de permitir publicar productos
    if request.user.perfilusuario.rol != 'vendedor':
        return redirect('catalogo')  # Redirigir al catálogo si no es vendedor

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.vendedor = request.user
            producto.save()
            return redirect('catalogo')  # Redirige al catálogo después de agregar el producto
    else:
        form = ProductoForm()

    return render(request, 'publicar_producto.html', {'form': form})

def catalogo(request):
    # Obtener todos los productos para mostrarlos en el catálogo
    productos = Producto.objects.all()
    return render(request, 'products.html', {'productos': productos})

def detalle_producto(request, id):
    # Obtener un producto específico por su ID
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'product_details.html', {'producto': producto})

# Función para mostrar el carrito
def carrito(request):
    carrito = request.session.get('carrito', [])  # Obtener los productos del carrito de la sesión
    carrito_vacio = len(carrito) == 0  # Verificar si el carrito está vacío
    total = sum(item['precio'] * item['cantidad'] for item in carrito)

    context = {
        'productos': carrito,
        'carrito_vacio': carrito_vacio,
        'total': total,
    }
    return render(request, 'cart.html', context)

# Función para agregar productos al carrito
def agregar_al_carrito(request, id):
    carrito = request.session.get('carrito', {})
    carrito[id] = carrito.get(id, 0) + 1  # Aumentar la cantidad del producto o agregarlo

    request.session['carrito'] = carrito  # Guardar el carrito actualizado en la sesión
    return redirect('carrito')

# Función para vaciar el carrito
def vaciar_carrito(request):
    request.session['carrito'] = {}  # Limpiar el carrito en la sesión
    return redirect('carrito')

def checkout(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        return redirect('catalogo')

    total = 0
    productos = []

    # Calcular el total y crear lista de productos
    for id, cantidad in carrito.items():
        producto = Producto.objects.get(id=id)
        subtotal = producto.precio * cantidad
        total += subtotal
        productos.append({'producto': producto, 'cantidad': cantidad, 'subtotal': subtotal})

    if request.method == 'POST':
        # Crear la orden
        orden = Orden.objects.create(usuario=request.user, total=total)
        for item in productos:
            DetalleOrden.objects.create(
                orden=orden,
                producto=item['producto'],
                cantidad=item['cantidad'],
                subtotal=item['subtotal']
            )

        # Vaciar el carrito después de la compra
        request.session['carrito'] = {}

        # Enviar correo de confirmación al usuario
        send_mail(
            'Confirmación de Compra - Horus',
            f'Tu orden #{orden.id} ha sido confirmada. Total: ${total}.',
            'tu-email@gmail.com',
            [request.user.email],
            fail_silently=False,
        )

        return redirect('catalogo')

    return render(request, 'checkout.html', {'productos': productos, 'total': total})

@login_required
def historial_pedidos(request):
    # Obtener todos los pedidos del usuario actual
    pedidos = Orden.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'historial.html', {'pedidos': pedidos})
