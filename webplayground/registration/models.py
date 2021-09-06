from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
class Profile(models.Model):
    avatar = models.ImageField(upload_to='profiles', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True, max_length=255)
    # Solo puede haber un perfil por cada usuario
    user = models.OneToOneField(User, on_delete=models.CASCADE)


"""
Signals => Las señales son eventos a ejecutar cuando algo ocurra en un modelo

@receiver(tipo_de_señal, sender=Modelo a escuchar el evento)
"""


@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    # Se valida si viene created en kwargs, solo se llama cuando se crea por lo tanto las demas veces
    # que se modifiquen el modelo no se enviara y no se actualizara
    if kwargs.get('created', False):
        Profile.objects.get_or_create(instance)
        print("Se creo un usuario y perfil por señal")

