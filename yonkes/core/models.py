from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.utils.timesince import timesince

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
    ESTATUS_CHOICES = [
        ('disponible', 'Disponible'),
        ('en_trato', 'En Trato'),
        ('vendido', 'Vendido'),
    ]
    
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50)
    marca = models.CharField(max_length=100, default="Desconocida")
    modelo = models.CharField(max_length=100, default="Desconocido")
    año = models.CharField(max_length=4, default="2020")
    motor = models.CharField(max_length=50, default="N/A")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Nuevo campo de estatus
    estatus = models.CharField(
        max_length=10,
        choices=ESTATUS_CHOICES,
        default='disponible',
    )

    def days_since_created(self):
        return (now() - self.created_at).days
    
    @property
    def time_since_created(self):
        time_difference = now() - self.created_at

        if time_difference.days >= 1:
            return f"Publicado hace {time_difference.days} día(s)"
        elif time_difference.seconds >= 3600:
            hours = time_difference.seconds // 3600
            return f"Publicado hace {hours} hora(s)"
        elif time_difference.seconds >= 60:
            minutes = time_difference.seconds // 60
            return f"Publicado hace {minutes} minuto(s)"
        else:
            return "Publicado hace unos segundos"
        
    @property
    def time_since_created(self):
        return timesince(self.fecha_creacion)


    def __str__(self):
        return self.nombre
    
class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='productos/imagenes/')

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"