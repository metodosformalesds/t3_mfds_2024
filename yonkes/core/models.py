from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.PositiveIntegerField(null=True, blank=True)  # Permite valores nulos y en blanco
    address = models.CharField(max_length=255, blank=True, null=True)  # Para OpenStreetMap
    phone_number = models.CharField(max_length=15)  # Para WhatsApp
    ROLE_CHOICES = (
        ('buyer', 'Comprador'),
        ('seller', 'Vendedor'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    is_profile_complete = models.BooleanField(default=False)  # Indica si el perfil está completo

    def __str__(self):
        return self.username
