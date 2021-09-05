from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    avatar = models.ImageField(upload_to='profiles', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True, max_length=255)
    # Solo puede haber un perfil por cada usuario
    user = models.OneToOneField(User, on_delete=models.CASCADE)