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
import stripe
from io import BytesIO
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import paypalrestsdk
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from .models import Producto
from django.http import HttpRequest
from .models import PerfilUsuario
from .models import Yonke

def get_client_ip(request):
    if not isinstance(request, HttpRequest):
        return None
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Configuración de Stripe con tu clave secreta
stripe.api_key = settings.STRIPE_SECRET_KEY

# Configuración de PayPal
paypalrestsdk.configure({
    "mode": "sandbox",  # Cambiar a 'live' en producción
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})

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

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from .forms import YonkeroSignupForm

def yonkero_signup(request):
    if request.method == 'POST':
        signup_form = YonkeroSignupForm(request.POST)
        if signup_form.is_valid():
            email = signup_form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Este correo electrónico ya está registrado. Por favor, usa otro o inicia sesión.')
            else:
                try:
                    user = signup_form.save(request)
                    messages.success(request, 'Tu cuenta de Yonkero ha sido creada exitosamente.')
                    return redirect('catalogo')
                except IntegrityError:
                    messages.error(request, 'Hubo un error al procesar tu registro. Intenta nuevamente.')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario de registro.')
    else:
        signup_form = YonkeroSignupForm()

    return render(request, 'yonkero_signup.html', {'signup_form': signup_form})

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

@csrf_exempt
def stripe_checkout(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = data.get('amount', 0)

            amount_in_cents = int(float(amount))

            if amount_in_cents > 99999999:
                return JsonResponse({'error': 'El monto total excede el límite permitido por Stripe.'}, status=400)

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Carrito de Compras',
                        },
                        'unit_amount': amount_in_cents,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/stripe/success/'),
                cancel_url=request.build_absolute_uri('/carrito/'),
            )
            return JsonResponse({'id': session.id})

        except stripe.error.StripeError as e:
            return JsonResponse({'error': f'Error de Stripe: {e.user_message}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Error del servidor: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Orden, DetalleOrden

@login_required
def stripe_success(request):
    try:
        # Recuperar la última orden del usuario autenticado
        ultima_orden = Orden.objects.filter(usuario=request.user).latest('fecha')
        detalles = DetalleOrden.objects.filter(orden=ultima_orden)

        # Calcular subtotal, impuesto y total directamente desde los detalles de la orden
        subtotal = sum(detalle.subtotal for detalle in detalles)
        impuesto = round(subtotal * 0.1, 2)  # Calcular 10% de impuesto
        total = round(subtotal + impuesto, 2)  # Total con impuestos incluidos

        # Pasar los datos al contexto
        context = {
            "message": "Pago completado exitosamente con Stripe",
            "orden": ultima_orden,
            "detalles": detalles,
            "subtotal": subtotal,
            "impuesto": impuesto,
            "total": total,
        }
        return render(request, 'historial_compras.html', context)
    except Orden.DoesNotExist:
        # Redirige al catálogo si no se encuentra una orden
        return redirect('catalogo')

@login_required
def paypal_success(request):
    """
    Maneja la página de éxito después de un pago con PayPal.
    """
    try:
        # Recuperar la última orden del usuario autenticado
        ultima_orden = Orden.objects.filter(usuario=request.user).latest('fecha')
        detalles = DetalleOrden.objects.filter(orden=ultima_orden)

        # Calcular subtotal, impuesto y total directamente desde los detalles de la orden
        subtotal = sum(detalle.subtotal for detalle in detalles)
        impuesto = round(subtotal * 0.1, 2)  # Calcular 10% de impuesto
        total = round(subtotal + impuesto, 2)  # Total con impuestos incluidos

        # Pasar los datos al contexto
        context = {
            "message": "Pago completado exitosamente con Stripe",
            "orden": ultima_orden,
            "detalles": detalles,
            "subtotal": subtotal,
            "impuesto": impuesto,
            "total": total,
        }
        return render(request, 'historial_compras.html', context)
    except Orden.DoesNotExist:
        # Redirige al catálogo si no se encuentra una orden
        return redirect('catalogo')

@csrf_exempt
def paypal_checkout(request):
    if request.method == 'POST':
        try:
            total = float(request.POST.get('amount', 0))
            if total <= 0:
                return JsonResponse({'error': 'El monto debe ser mayor a 0'}, status=400)

            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal",
                },
                "redirect_urls": {
                    "return_url": request.build_absolute_uri('/paypal/success/'),
                    "cancel_url": request.build_absolute_uri('/carrito/'),
                },
                "transactions": [{
                    "amount": {
                        "total": f"{total:.2f}",
                        "currency": "USD",
                    },
                    "description": "Compra en Horuz Autopartes",
                }],
            })

            if payment.create():
                for link in payment.links:
                    if link.rel == "approval_url":
                        approval_url = link.href
                        return JsonResponse({"approval_url": approval_url})
                return JsonResponse({"error": "No se encontró el enlace de aprobación"}, status=500)
            else:
                return JsonResponse({"error": payment.error}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)


def stripe_success(request):
    return render(request, 'historial_compras.html', {"message": "Pago completado exitosamente con Stripe"})


def stripe_cancel(request):
    return redirect('carrito')  # Cambia 'carrito' al nombre de tu URL de carrito


def paypal_success(request):
    return render(request, 'historial_compras.html', {"message": "Pago completado exitosamente con PayPal"})

def paypal_cancel(request):
    return redirect('carrito')  # Cambia 'carrito' al nombre de tu URL de carrito

import logging
logger = logging.getLogger(__name__)

def checkout(request):
    carrito = request.session.get('carrito', [])
    if not carrito:
        logger.warning("El carrito está vacío. Redirigiendo al catálogo.")
        return redirect('catalogo')

    # Calcular el total del carrito
    try:
        total = sum(item['precio'] * item['cantidad'] for item in carrito)
    except KeyError as e:
        logger.error(f"Error al calcular el total del carrito: {e}")
        return redirect('catalogo')  # Redirige en caso de un error inesperado

    if request.method == 'POST':
        try:
            # Crear la orden
            orden = Orden.objects.create(usuario=request.user, total=total)
            logger.info(f"Orden creada: {orden}")

            # Asociar productos al detalle de la orden directamente desde el carrito
            for item in carrito:
                DetalleOrden.objects.create(
                    orden=orden,
                    producto_nombre=item['titulo'],  # Nombre del producto desde JSON
                    producto_precio=item['precio'],  # Precio del producto desde JSON
                    producto_imagen=item.get('pictures', [{}])[0].get('url', ''),  # Primera imagen, si existe
                    cantidad=item['cantidad'],
                    subtotal=item['precio'] * item['cantidad']
                )
            logger.info(f"Detalles de la orden asociados: {orden.detalleorden_set.all()}")

            # Vaciar el carrito
            request.session['carrito'] = []
            logger.info("Carrito vaciado después de la compra.")

            return redirect('stripe_success')

        except Exception as e:
            logger.error(f"Error al procesar la orden: {e}")
            return redirect('catalogo')  # Redirige en caso de un error inesperado

    # Renderizar la página de checkout
    context = {
        'productos': carrito,
        'total': total,
    }
    return render(request, 'checkout.html', context)

def generate_invoice_pdf(orden):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    pdf.drawString(100, 800, f"Factura - Orden #{orden.id}")
    pdf.drawString(100, 780, f"Fecha: {orden.fecha}")
    pdf.drawString(100, 760, f"Total: ${orden.total}")

    y_position = 740
    for item in orden.detalleorden_set.all():
        pdf.drawString(100, y_position, f"Producto: {item.producto} | Cantidad: {item.cantidad} | Subtotal: ${item.subtotal}")
        y_position -= 20

    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=f"factura_{orden.id}.pdf")

@login_required
def historial_pedidos(request):
    pedidos = Orden.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'historial-compras.html', {'pedidos': pedidos})

# Historial de compras
@login_required
def historial_compras(request):
    compras = Orden.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'historial_compras.html', {'compras': compras})

# Generación de PDF
@login_required
def descargar_recibo(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id, usuario=request.user)

    # Plantilla para el PDF
    template_path = 'recibo_pdf.html'
    context = {
        'orden': orden,
        'detalles': orden.detalleorden_set.all(),
    }

    # Renderizar HTML a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="recibo_{orden.id}.pdf"'
    template = render_to_string(template_path, context)
    pisa_status = pisa.CreatePDF(template, dest=response)

    if pisa_status.err:
        return HttpResponse('Hubo un error al generar el PDF.', status=500)

    return response

@login_required
def mi_yonke(request):
    # Verificar si el usuario es "vendedor"
    perfil = PerfilUsuario.objects.filter(usuario=request.user, rol='vendedor').first()
    if not perfil:
        return redirect('catalogo')  # Redirige a "catalogo" si no es vendedor

    # Obtener la información del Yonke asociado al usuario
    yonke = Yonke.objects.filter(nombre=request.user.username).first()

    # Obtener los productos asociados al vendedor
    productos = Producto.objects.filter(vendedor=request.user)

    # Renderizar el contexto
    context = {
        'yonke': yonke,
        'productos': productos,
    }
    return render(request, 'mi_yonke.html', context)

def header_context(request):
    # Si el usuario está autenticado, incluye datos personalizados
    if request.user.is_authenticated:
        perfil = getattr(request.user, 'perfilusuario', None)
        return {
            'is_authenticated': True,
            'username': request.user.username,
            'rol': perfil.rol if perfil else None,
        }
    return {'is_authenticated': False}


