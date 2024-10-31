from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Configuración de los campos que aparecerán al ver o editar un usuario existente
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('age', 'address', 'phone_number', 'role', 'is_profile_complete')
        }),
    )

    # Configuración de los campos al agregar un nuevo usuario desde el panel de administración
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {
            'fields': ('age', 'address', 'phone_number', 'role')
        }),
    )

    # Campos que se muestran en la lista de usuarios
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_profile_complete']

# Registrar el modelo de usuario extendido en el panel de administración
admin.site.register(CustomUser, CustomUserAdmin)
