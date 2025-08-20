from django.db import models
from accounts.models import User
from flashcards.models import Deck


class Tag(models.Model):
    name = models.CharField(max_length=32)
    
    def __str__(self):
        return self.name


class Listing(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='listings')
    description = models.CharField(max_length=1024)
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    tags = models.ManyToManyField(Tag, related_name='listings')
    
    def __str__(self):
        return f'{self.deck} listing created by {self.created_by}'
    

class ListingImage(models.Model):
    image = models.ImageField(upload_to='listing_images/')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')