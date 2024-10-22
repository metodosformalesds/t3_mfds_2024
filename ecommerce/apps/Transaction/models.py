from django.db import models

# Create your models here.
class Transaction(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='transactions')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='transactions')
    auto_part = models.ForeignKey(AutoPart, on_delete=models.CASCADE, related_name='transactions')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=50, choices=[('pending', 'Pendiente'), ('completed', 'Completado')])

    def __str__(self):
        return f'Transacción {self.id} - {self.auto_part.name}'
