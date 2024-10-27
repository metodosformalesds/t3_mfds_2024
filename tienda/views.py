from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Orden, DetalleOrden
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'tienda/index.html')

def catalogo(request):
    productos = Producto.objects.all()  # Asegúrate de obtener todos los productos
    return render(request, 'tienda/catalogo.html', {'productos': productos})

def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)  # Obtener un producto específico
    return render(request, 'tienda/detalle_producto.html', {'producto': producto})

# Función para mostrar el carrito
def carrito(request):
    carrito = request.session.get('carrito', {})  # Recuperar el carrito de la sesión
    productos = []
    total = 0

    for id, cantidad in carrito.items():
        producto = Producto.objects.get(id=id)
        subtotal = producto.precio * cantidad
        total += subtotal
        productos.append({'producto': producto, 'cantidad': cantidad, 'subtotal': subtotal})

    return render(request, 'tienda/carrito.html', {'productos': productos, 'total': total})

# Función para agregar productos al carrito
def agregar_al_carrito(request, id):
    carrito = request.session.get('carrito', {})

    # Incrementar la cantidad si ya existe, o agregarlo por primera vez
    if str(id) in carrito:
        carrito[str(id)] += 1
    else:
        carrito[str(id)] = 1

    request.session['carrito'] = carrito  # Guardar el carrito en la sesión
    return redirect('catalogo')

# Función para vaciar el carrito
def vaciar_carrito(request):
    request.session['carrito'] = {}  # Limpiar la sesión del carrito
    return redirect('carrito')

def checkout(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        return redirect('catalogo')

    total = 0
    productos = []

    # Crear lista de productos y calcular el total
    for id, cantidad in carrito.items():
        producto = Producto.objects.get(id=id)
        subtotal = producto.precio * cantidad
        total += subtotal
        productos.append({'producto': producto, 'cantidad': cantidad, 'subtotal': subtotal})

    if request.method == 'POST':
        orden = Orden.objects.create(usuario=request.user, total=total)
        for item in productos:
            DetalleOrden.objects.create(
                orden=orden,
                producto=item['producto'],
                cantidad=item['cantidad'],
                subtotal=item['subtotal']
            )
        request.session['carrito'] = {}  # Vaciar el carrito después del checkout
        return redirect('catalogo')

    return render(request, 'tienda/checkout.html', {'productos': productos, 'total': total})

def historial_pedidos(request):
    pedidos = Orden.objects.filter(usuario=request.user).order_by('-fecha')  # Pedidos del usuario
    return render(request, 'tienda/historial.html', {'pedidos': pedidos})

