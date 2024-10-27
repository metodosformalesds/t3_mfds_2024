from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from tienda.models import PerfilUsuario

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        # Solo crea el perfil si el usuario es nuevo
        PerfilUsuario.objects.create(usuario=instance, rol='comprador')
    else:
        # Guarda el perfil si ya existe
        if hasattr(instance, 'perfilusuario'):
            instance.perfilusuario.save()