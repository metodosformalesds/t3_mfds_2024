from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CompleteProfileForm

# Vista para la página Home con lógica de autenticación
def home(request):
    user_name = None
    if request.user.is_authenticated:
        user_name = request.user.get_full_name() or request.user.username

    return render(request, 'home.html', {'user_name': user_name})

@login_required
def complete_profile(request):
    user = request.user
    if user.street and user.city and user.role:  # Verifica si ya se ha completado el perfil
        if user.role == 'vendedor':
            return redirect('vendedor_panel_url')  # Redirige al panel del vendedor
        elif user.role == 'comprador':
            return redirect('comprador_panel_url')  # Redirige al panel del comprador
        else:
            return redirect('/')  # O redirige a una página por defecto si el rol no está definido

    if request.method == 'POST':
        form = CompleteProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
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
    return render(request, 'core/vendedor_panel.html')

# Panel de comprador
@login_required
def comprador_panel(request):
    return render(request, 'core/comprador_panel.html')

# Nueva vista: Redirección después de iniciar sesión
@login_required
def redirect_after_login(request):
    user = request.user
    if user.role == 'vendedor':
        return redirect('vendedor_panel_url')
    elif user.role == 'comprador':
        return redirect('comprador_panel_url')
    else:
        return redirect('/')  # Redirige al Home si el rol no está definido
