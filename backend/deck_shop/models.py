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
    likes = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    tags = models.ManyToManyField(Tag, null=True, blank=True, related_name='listings')
    
    def __str__(self):
        return f'{self.deck} listing created by {self.created_by}'
    

class ListingImage(models.Model):
    image = models.ImageField(upload_to='listing_images/')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    

class Reaction(models.Model):
    is_like = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Reactions')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='Reactions')
    
    def save(self, *args, **kwargs):
        try:
            listing = self.listing
        except Listing.DoesNotExist:
            print('Reaction does not have an existing listing.')
        else:
            super().save(*args, **kwargs)
            if self.is_like:
                listing.likes += 1
            else:
                listing.likes -= 1
            listing.save(update_fields=['likes'])