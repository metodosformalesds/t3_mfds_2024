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

class Transaction(models.Model):
    TransactionID = models.AutoField(primary_key=True)
    BuyerID = models.ForeignKey(Buyer, on_delete=models.CASCADE)  # Relación con Buyer
    SellerID = models.ForeignKey(Seller, on_delete=models.CASCADE)  # Relación con Seller
    AutoPartID = models.ForeignKey(AutoPart, on_delete=models.CASCADE)  # Relación con AutoPart
    Date = models.DateTimeField()  # Fecha y hora de la transacción
    TotalAmount = models.DecimalField(max_digits=10, decimal_places=2)  # Monto total con 2 decimales
    PaymentMethod = models.CharField(max_length=50)  # Método de pago (Ej: 'Tarjeta', 'Paypal')
    TransactionStatus = models.CharField(max_length=50)  # Estado de la transacción (Ej: 'Completada', 'Pendiente')

    def __str__(self):
        return f"Transaction {self.TransactionID} - {self.BuyerID.name} to {self.SellerID.name}"

class Payment(models.Model):
    PaymentID = models.AutoField(primary_key=True)
    TransactionID = models.ForeignKey('Transaction', on_delete=models.CASCADE)  # Relación con Transaction
    Amount = models.DecimalField(max_digits=10, decimal_places=2)  # Monto pagado
    PaymentMethod = models.CharField(max_length=50)  # Método de pago
    PaymentStatus = models.CharField(max_length=20)  # Estado del pago (Approved, Rejected, Pending)
    PaymentDate = models.DateTimeField()  # Fecha de pago

    def __str__(self):
        return f"Payment {self.PaymentID} - {self.PaymentStatus}"
