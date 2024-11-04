from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Producto
from .forms import CompleteProfileForm, ProductoForm

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
            return redirect('comprador_panel_url')
    
    # Si el perfil no está completo, muestra el formulario para completarlo
    if request.method == 'POST':
        form = CompleteProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # Una vez completado el perfil, redirige al panel correspondiente
            if user.role == 'vendedor':
                return redirect('vendedor_panel_url')
            elif user.role == 'comprador':
                return redirect('comprador_panel_url')
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
        return redirect('comprador_panel_url')
    else:
        return redirect('/')  # O maneja el caso de redirección por defecto si algo sale mal

#PRODUCTOS
@login_required
def listar_productos(request):
    productos = Producto.objects.filter(vendedor=request.user)
    return render(request, 'core/listar_productos.html', {'productos': productos})

@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.vendedor = request.user  # Asigna el usuario actual como vendedor
            producto.save()
            # Redirige al panel de vendedor después de añadir el producto
            return redirect('vendedor_panel_url')  # Asegúrate de que 'vendedor_panel_url' sea el nombre correcto
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
            return redirect('listar_productos')
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