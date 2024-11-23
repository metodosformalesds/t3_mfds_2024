from django.contrib.auth.models import User
from django.db import models
import uuid

class Producto(models.Model):
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el vendedor
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='categorias/', blank=True, null=True)

    def __str__(self):
        return self.nombre


class Orden(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    numero_recibo = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # UUID como identificador único

    def __str__(self):
        return f"Orden #{self.id} - Recibo: {self.numero_recibo}"


class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)  # Relación con la orden
    producto_nombre = models.CharField(max_length=255)  # Guardar el nombre del producto
    producto_precio = models.DecimalField(max_digits=10, decimal_places=2)  # Guardar el precio del producto
    producto_imagen = models.URLField(max_length=500, null=True, blank=True)  # Guardar la URL de la imagen del producto
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle - Orden #{self.orden.id} - Producto: {self.producto_nombre}"


class PerfilUsuario(models.Model):
    ROLES = (
        ('comprador', 'Comprador'),
        ('vendedor', 'Vendedor'),
    )

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación uno a uno con el usuario
    rol = models.CharField(max_length=10, choices=ROLES, default='comprador')

    def __str__(self):
        return f"{self.usuario.username} - {self.get_rol_display()}"


class Yonke(models.Model):
    vendedor = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación con el vendedor
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    def obtener_productos(self):
        return Producto.objects.filter(vendedor=self.vendedor)
