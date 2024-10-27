# tienda/models.py
from django.contrib.auth.models import User  
from django.db import models

class Producto(models.Model):
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)  # Ahora no permite nulos
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre

class Orden(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Orden #{self.id} - {self.usuario.username}"

class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto.nombre} (x{self.cantidad})"

class PerfilUsuario(models.Model):
    ROLES = (
        ('comprador', 'Comprador'),
        ('vendedor', 'Vendedor'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Cambiado a ForeignKey
    rol = models.CharField(max_length=10, choices=ROLES, default='comprador')

    def __str__(self):
        return f"{self.usuario.username} - {self.get_rol_display()}"
