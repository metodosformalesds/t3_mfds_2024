from django.contrib.auth.models import AbstractUser
from django.db import models

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

