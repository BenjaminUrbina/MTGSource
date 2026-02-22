from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import usuario_mtg


@receiver(post_save, sender=User)
def crear_perfil_usuario_mtg(sender, instance, created, **kwargs):
    """
    Se ejecuta cada vez que se guarda un User.
    Si el User fue creado recién (created=True), creamos su perfil UsuarioMTG.
    """
    if created:
        usuario_mtg.objects.create(
            user=instance,
            nombre=instance.username  # por defecto, usa el username como nombre
        )
