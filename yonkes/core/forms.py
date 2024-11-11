from django import forms
from .models import CustomUser, Producto

class CompleteProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name',
            'street', 'street_number', 'apartment_number',
            'neighborhood', 'postal_code', 'city', 'state', 'country',
            'phone_number', 'role'
        ]
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'street': 'Calle',
            'street_number': 'Número exterior',
            'apartment_number': 'Número interior (opcional)',
            'neighborhood': 'Colonia o barrio',
            'postal_code': 'Código postal',
            'city': 'Ciudad',
            'state': 'Estado/Provincia',
            'country': 'País',
            'phone_number': 'Número de teléfono',
            'role': 'Rol',
        }
        widgets = {
            'street': forms.TextInput(attrs={'placeholder': 'Calle'}),
            'street_number': forms.TextInput(attrs={'placeholder': 'Número exterior'}),
            'apartment_number': forms.TextInput(attrs={'placeholder': 'Número interior (opcional)'}),
            'neighborhood': forms.TextInput(attrs={'placeholder': 'Colonia o barrio'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Código postal'}),
            'city': forms.TextInput(attrs={'placeholder': 'Ciudad'}),
            'state': forms.TextInput(attrs={'placeholder': 'Estado/Provincia'}),
            'country': forms.TextInput(attrs={'placeholder': 'País'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Número de teléfono'}),
            'role': forms.Select(choices=[('vendedor', 'Vendedor'), ('comprador', 'Comprador')]),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'descripcion',
            'precio',
            'categoria',
            'marca',  # Añade el nuevo campo
            'modelo',  # Añade el nuevo campo
            'año',     # Añade el nuevo campo
            'motor',   # Añade el nuevo campo
           'estatus',  # Reemplaza 'disponible' por 'estatus'
        ]

