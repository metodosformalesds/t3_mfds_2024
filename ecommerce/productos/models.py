from django.db import models

# Create your models here.
class AutoPart(models.Model):
    Name = models.CharField(max_length=255)
    Description = models.TextField()
    Price = models.DecimalField(max_digits=10, decimal_places=2)  # Precio con 2 decimales
    Condition = models.CharField(max_length=50)  # Condición (Ej: 'Nuevo', 'Usado')
    Brand = models.CharField(max_length=100)
    Model = models.CharField(max_length=100)
    Year = models.IntegerField()  # Año del auto
    CarPartType = models.CharField(max_length=100)  # Tipo de autoparte (Ej: 'Motor', 'Llantas')
    Image = models.ImageField(upload_to='autoparts/images/')  # Ruta de la imagen
    Stock = models.IntegerField()  # Cantidad en inventario

    def __str__(self):
        return self.Name