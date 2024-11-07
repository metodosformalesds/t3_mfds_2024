# tienda/views.py

from django.shortcuts import render, redirect
from .models import Orden, DetalleOrden, Categoria
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
import requests

def index(request):
    # Obtener todas las categorías desde la base de datos para mostrarlas en el index
    categorias = Categoria.objects.all()
    return render(request, 'index.html', {'categorias': categorias})

def account_view(request):
    # Vista unificada para el inicio de sesión y registro
    return render(request, 'account.html')

@login_required
def publicar_producto(request):
    # Eliminar la lógica de productos locales y la publicación de productos,
    # ya que ahora solo se trabaja con la API de Mercado Libre.
    return redirect('catalogo')

def catalogo(request):
    # URL de la API que está sirviendo los productos (Node.js)
    api_url = 'http://localhost:3000/autopartes'

    try:
        # Realiza la solicitud a la API
        response = requests.get(api_url)
        response.raise_for_status()  # Verifica si la respuesta tiene errores
        
        # Convierte la respuesta JSON en un objeto de Python
        productos = response.json()
    except requests.exceptions.RequestException as e:
        # En caso de error, loguea y muestra un mensaje de error en la plantilla
        print(f"Error al obtener productos de la API: {e}")
        productos = []  # Vacía la lista de productos para manejar el error adecuadamente
    
    # Renderiza la plantilla con los productos obtenidos
    return render(request, 'products.html', {'productos': productos})

def detalle_producto(request, id):
    # Obtener detalles del producto desde la API de Node.js
    api_url = f'http://localhost:3000/productos/{id}'

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        producto_data = response.json()  # El producto es un diccionario con la información de la API
        producto_data['producto_local'] = False
    except requests.exceptions.RequestException as e:
        # Si hay un error al obtener el producto, mostrar un mensaje en la plantilla
        print(f"Error al obtener producto de la API: {e}")
        return render(request, 'product_details.html', {'error': 'No se pudo cargar el producto. Intente más tarde.'})

    # Renderiza la plantilla con los detalles del producto
    return render(request, 'product_details.html', {'producto': producto_data})

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
    # Obtener la información del producto y agregarla al carrito
    carrito = request.session.get('carrito', [])
    api_url = f'http://localhost:3000/productos/{id}'

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        producto = response.json()
        producto_info = {
            'id': producto['id'],
            'titulo': producto['titulo'],
            'precio': producto['precio'],
            'imagen': producto['imagen'],
            'cantidad': 1
        }

        # Verificar si el producto ya está en el carrito
        for item in carrito:
            if item['id'] == producto_info['id']:
                item['cantidad'] += 1
                break
        else:
            # Si no está, agregarlo al carrito
            carrito.append(producto_info)

        request.session['carrito'] = carrito  # Guardar el carrito actualizado en la sesión

    except requests.exceptions.RequestException as e:
        print(f"Error al obtener producto de la API para agregar al carrito: {e}")

    return redirect('carrito')

# Función para vaciar el carrito
def vaciar_carrito(request):
    request.session['carrito'] = []  # Limpiar el carrito en la sesión
    return redirect('carrito')

def checkout(request):
    carrito = request.session.get('carrito', [])
    if not carrito:
        return redirect('catalogo')

    total = sum(item['precio'] * item['cantidad'] for item in carrito)

    if request.method == 'POST':
        # Crear la orden
        orden = Orden.objects.create(usuario=request.user, total=total)
        for item in carrito:
            # Ya que solo usamos la API, el producto local será None
            DetalleOrden.objects.create(
                orden=orden,
                producto=None,
                cantidad=item['cantidad'],
                subtotal=item['precio'] * item['cantidad']
            )

        # Vaciar el carrito después de la compra
        request.session['carrito'] = []

        # Enviar correo de confirmación al usuario
        send_mail(
            'Confirmación de Compra - Horus',
            f'Tu orden #{orden.id} ha sido confirmada. Total: ${total}.',
            'tu-email@gmail.com',
            [request.user.email],
            fail_silently=False,
        )

        return redirect('catalogo')

    return render(request, 'checkout.html', {'productos': carrito, 'total': total})

@login_required
def historial_pedidos(request):
    # Obtener todos los pedidos del usuario actual
    pedidos = Orden.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'historial.html', {'pedidos': pedidos})
