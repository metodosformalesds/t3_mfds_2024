from django.shortcuts import render, redirect, get_object_or_404
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
import requests

def index(request):
    categorias = Categoria.objects.all()
    return render(request, 'index.html', {'categorias': categorias})

def account_view(request):
    return render(request, 'account.html')

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

def detalle_yonke(request, place_id):
    api_key = getattr(settings, "GOOGLE_MAPS_API_KEY", None)
    if not api_key:
        return render(request, "yonke_details.html", {"error": "Clave de API de Google Maps no configurada."})

    # Consultar detalles del lugar desde Place Details API
    place_details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"

    try:
        # Obtener los datos del lugar
        response = requests.get(place_details_url)
        response_data = response.json()

        if response_data.get("status") != "OK":
            raise ValueError(f"Error en Place Details API: {response_data.get('status')}")

        result = response_data.get("result", {})
        direccion = result.get("formatted_address", "Dirección no disponible")
        nombre = result.get("name", "Nombre no disponible")
        descripcion = result.get("editorial_summary", {}).get("overview", "Descripción no disponible")
        imagen = result.get("photos", [{}])[0].get("photo_reference", "")

        # Usar Geocoding API para obtener las coordenadas a partir de la dirección
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={direccion}&key={api_key}"
        geocode_response = requests.get(geocode_url)
        geocode_data = geocode_response.json()

        if geocode_data.get("status") != "OK":
            raise ValueError(f"Error en Geocoding API: {geocode_data.get('status')}")

        # Extraer las coordenadas del resultado de Geocoding API
        geometry = geocode_data["results"][0]["geometry"]["location"]
        latitud = geometry.get("lat", 0)
        longitud = geometry.get("lng", 0)

        # Generar URL para la imagen, si está disponible
        if imagen:
            imagen_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={imagen}&key={api_key}"
        else:
            imagen_url = "https://via.placeholder.com/300"

        # Crear el diccionario de datos para el template
        yonke_data = {
            "place_id": place_id,
            "nombre": nombre,
            "direccion": direccion,
            "descripcion": descripcion,
            "latitud": latitud,
            "longitud": longitud,
            "imagen": imagen_url,
        }

        print(f"Datos del Yonke obtenidos: {yonke_data}")

    except Exception as e:
        print(f"Error al procesar el Yonke: {e}")
        return render(request, "yonke_details.html", {"error": "No se pudieron cargar los datos del Yonke."})

    return render(request, "yonke_details.html", {"yonke": yonke_data})

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
