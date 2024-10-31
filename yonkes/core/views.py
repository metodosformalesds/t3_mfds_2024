from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomSignupForm

# Vista para la página Home con lógica de autenticación
def home(request):
    user_name = None
    if request.user.is_authenticated:
        user_name = request.user.get_full_name() or request.user.username

    return render(request, 'home.html', {'user_name': user_name})

@login_required
def complete_profile(request):
    user = request.user
    if user.is_profile_complete:
        return redirect('/')

    if request.method == 'POST':
        form = CustomSignupForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            user.is_profile_complete = True
            user.save()
            return redirect('/')
    else:
        form = CustomSignupForm(instance=user)
    
    return render(request, 'account/complete_profile.html', {'form': form})
