from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Orden, DetalleOrden
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import ProductoForm
from django.contrib.auth.models import User
from tienda.models import PerfilUsuario
from .models import Categoria  # Asegúrate de tener este modelo definido

def index(request):
    categorias = Categoria.objects.all()  # Obtener todas las categorías desde la base de datos
    return render(request, 'index.html', {'categorias': categorias})


@login_required
def publicar_producto(request):
    if request.user.perfilusuario.rol != 'vendedor':
        return redirect('catalogo')  # Redirigir si no es vendedor

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.vendedor = request.user
            producto.save()
            return redirect('catalogo')  # Redirige al catálogo después de agregar
    else:
        form = ProductoForm()

    return render(request, 'tienda/publicar_producto.html', {'form': form})

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

        # Vaciar el carrito
        request.session['carrito'] = {}

        # Enviar correo de confirmación
        send_mail(
            'Confirmación de Compra - Horus',
            f'Tu orden #{orden.id} ha sido confirmada. Total: ${total}.',
            'tu-email@gmail.com',
            [request.user.email],  # Enviar al correo del usuario
            fail_silently=False,
        )

        return redirect('catalogo')

    return render(request, 'tienda/checkout.html', {'productos': productos, 'total': total})

def historial_pedidos(request):
    pedidos = Orden.objects.filter(usuario=request.user).order_by('-fecha')  # Pedidos del usuario
    return render(request, 'tienda/historial.html', {'pedidos': pedidos})

from .forms import RegistroForm, PerfilForm

def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        rol = request.POST['rol']  # 'comprador' o 'vendedor'

        # Crear un nuevo usuario solo si no existe
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            # Crear el perfil con el rol correspondiente
            PerfilUsuario.objects.create(usuario=user, rol=rol)
            return redirect('login')  # Redirigir al login después del registro
        else:
            # Mostrar mensaje de error si el usuario ya existe
            return render(request, 'registro.html', {'error': 'El usuario ya existe.'})

    return render(request, 'registro.html')


