from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_profile_complete')

    def is_profile_complete(self, obj):
        # Aquí defines la lógica para determinar si el perfil está completo
        return bool(obj.street and obj.street_number and obj.city)

    is_profile_complete.boolean = True  # Esto muestra un icono booleano en el admin

admin.site.register(CustomUser, CustomUserAdmin)