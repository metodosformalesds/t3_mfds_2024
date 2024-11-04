from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    street = models.CharField(max_length=255)
    street_number = models.CharField(max_length=10)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    neighborhood = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=[('vendedor', 'Vendedor'), ('comprador', 'Comprador')])



User = get_user_model()

class Producto(models.Model):
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50)
    marca = models.CharField(max_length=100, default="Desconocida")  # Valor por defecto
    modelo = models.CharField(max_length=100, default="Desconocido")  # Valor por defecto
    año = models.CharField(max_length=4, default="2020")  # Valor por defecto
    motor = models.CharField(max_length=50, default="N/A")  # Valor por defecto
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='productos/imagenes/')

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"