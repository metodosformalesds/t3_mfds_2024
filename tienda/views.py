from django.shortcuts import render, redirect
from .models import Orden, DetalleOrden, Categoria
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from allauth.account.forms import LoginForm, SignupForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
import json
import os

def index(request):
    categorias = Categoria.objects.all()
    return render(request, 'index.html', {'categorias': categorias})

def account_view(request):
    # Página de selección de tipo de cuenta (Cliente/Yonkero)
    return render(request, 'account.html')

# Vistas para Login y Registro de Cliente
def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username_or_email = request.POST.get('login')
            password = request.POST.get('password')
            user = authenticate(request, username=username_or_email, password=password)
            if user is None:
                try:
                    user_instance = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_instance.username, password=password)
                except User.DoesNotExist:
                    user = None

            if user is not None:
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, 'Has iniciado sesión exitosamente.')
                return redirect('catalogo')
            else:
                messages.error(request, 'Error al iniciar sesión. Por favor, verifica tus credenciales.')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario de inicio de sesión.')

    else:
        login_form = LoginForm()

    context = {'login_form': login_form}
    return render(request, 'user_login.html', context)

def user_signup(request):
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            try:
                user = signup_form.save(request)
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, 'Tu cuenta ha sido creada exitosamente.')
                return redirect('catalogo')
            except IntegrityError:
                messages.error(request, 'Este correo electrónico ya está registrado. Por favor, usa otro o inicia sesión.')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario de registro.')
    else:
        signup_form = SignupForm()

    context = {'signup_form': signup_form}
    return render(request, 'user_signup.html', context)

# Vistas para Login y Registro de Yonkero
def yonkero_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username_or_email = request.POST.get('login')
            password = request.POST.get('password')
            user = authenticate(request, username=username_or_email, password=password)
            if user is None:
                try:
                    user_instance = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_instance.username, password=password)
                except User.DoesNotExist:
                    user = None

            if user is not None:
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, 'Has iniciado sesión exitosamente como Yonkero.')
                return redirect('catalogo')
            else:
                messages.error(request, 'Error al iniciar sesión. Por favor, verifica tus credenciales.')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario de inicio de sesión.')

    else:
        login_form = LoginForm()

    context = {'login_form': login_form}
    return render(request, 'yonkero_login.html', context)

def yonkero_signup(request):
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            try:
                user = signup_form.save(request)
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, 'Tu cuenta de Yonkero ha sido creada exitosamente.')
                return redirect('catalogo')
            except IntegrityError:
                messages.error(request, 'Este correo electrónico ya está registrado. Por favor, usa otro o inicia sesión.')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario de registro.')
    else:
        signup_form = SignupForm()

    context = {'signup_form': signup_form}
    return render(request, 'yonkero_signup.html', context)

@login_required
def publicar_producto(request):
    return redirect('catalogo')

def catalogo(request):
    productos_path = os.path.join(settings.BASE_DIR, 'static/js/productos.json')

    try:
        with open(productos_path, 'r', encoding='utf-8') as file:
            productos = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al cargar productos desde productos.json: {e}")
        productos = []

    return render(request, 'products.html', {'productos': productos})

def detalle_producto(request, id):
    productos_path = os.path.join(settings.BASE_DIR, 'static/js/productos.json')

    try:
        with open(productos_path, 'r', encoding='utf-8') as file:
            productos = json.load(file)
            producto = next((p for p in productos if p['id'] == id), None)

        if not producto:
            return render(request, 'product_details.html', {'error': 'Producto no encontrado.'})

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al cargar productos desde productos.json: {e}")
        return render(request, 'product_details.html', {'error': 'No se pudo cargar el producto. Intente más tarde.'})

    return render(request, 'product_details.html', {'producto': producto})

def carrito(request):
    carrito = request.session.get('carrito', [])
    carrito_vacio = len(carrito) == 0
    total = sum(item['precio'] * item['cantidad'] for item in carrito)

    context = {
        'productos': carrito,
        'carrito_vacio': carrito_vacio,
        'total': total,
    }
    return render(request, 'cart.html', context)

def agregar_al_carrito(request, id):
    carrito = request.session.get('carrito', [])
    productos_path = os.path.join(settings.BASE_DIR, 'static/js/productos.json')

    try:
        with open(productos_path, 'r', encoding='utf-8') as file:
            productos = json.load(file)
            producto = next((p for p in productos if p['id'] == id), None)

        if not producto:
            return redirect('catalogo')

        producto_info = {
            'id': producto['id'],
            'titulo': producto['titulo'],
            'precio': producto['precio'],
            'imagen': producto['imagen'],
            'cantidad': 1
        }

        for item in carrito:
            if item['id'] == producto_info['id']:
                item['cantidad'] += 1
                break
        else:
            carrito.append(producto_info)

        request.session['carrito'] = carrito

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al cargar productos desde productos.json para agregar al carrito: {e}")

    return redirect('carrito')

def vaciar_carrito(request):
    request.session['carrito'] = []
    return redirect('carrito')

def checkout(request):
    carrito = request.session.get('carrito', [])
    if not carrito:
        return redirect('catalogo')

    total = sum(item['precio'] * item['cantidad'] for item in carrito)

    if request.method == 'POST':
        orden = Orden.objects.create(usuario=request.user, total=total)
        for item in carrito:
            DetalleOrden.objects.create(
                orden=orden,
                producto=None,
                cantidad=item['cantidad'],
                subtotal=item['precio'] * item['cantidad']
            )

        request.session['carrito'] = []

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
    pedidos = Orden.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'historial.html', {'pedidos': pedidos})
