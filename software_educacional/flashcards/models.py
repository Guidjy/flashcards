from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    imagem_de_perfil = models.URLField(blank=True, null=True, default="https://static.vecteezy.com/system/resources/previews/013/360/247/non_2x/default-avatar-photo-icon-social-media-profile-sign-symbol-vector.jpg")
    
    def __str__(self):
        return self.username
    

class Deck(models.Model):
    nome = models.CharField(max_length=140)
    criador = models.ForeignKey(User, on_delete=models.CASCADE)
    numero_de_cards = models.IntegerField(default=0)
    ordem_dos_cards = models.JSONField(dict, default=dict)
    likes = models.IntegerField(default=0)
    
    def __str__(self):
        return f'#{self.id}) \"{self.nome}\" - criado por {self.criador}'
    

class Tag(models.Model):
    nome = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.nome}'
    

class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    frente = models.CharField(max_length=280)
    tras = models.TextField(max_length=1200)
    imagem = models.URLField(blank=True, null=True)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f'#{self.id})  frente: \"{self.frente}\" / tras: \"{self.tras}\" / tag: {self.tag}'