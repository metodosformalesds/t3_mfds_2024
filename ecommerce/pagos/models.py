from django.db import models

class Subscription(models.Model):
    SubscriptionID = models.AutoField(primary_key=True)
    SellerID = models.ForeignKey(Seller, on_delete=models.CASCADE)  # Relación con Seller
    SubscriptionType = models.CharField(max_length=100)  # Tipo de suscripción (Ej: 'Básico', 'Premium')
    Price = models.DecimalField(max_digits=10, decimal_places=2)  # Precio con dos decimales
    StartDate = models.DateField()  # Fecha de inicio de la suscripción
    EndDate = models.DateField()  # Fecha de fin de la suscripción

    def __str__(self):
        return f"{self.SubscriptionType} - {self.SellerID.name}"
