from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    imagem_de_perfil = models.ImageField(blank=True, null=True)
