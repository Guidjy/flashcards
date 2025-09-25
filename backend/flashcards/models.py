from django.db import models
from accounts.models import User


class Deck(models.Model):
    name = models.CharField(max_length=64)
    card_count = models.IntegerField(default=0)
    card_order = models.JSONField(default=dict, null=True)
    
    owned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decks')
    
    def __str__(self):
        return f'{self.name}'
    

# peep this model in the future cuz there's some important stuff about concurrency, side effects and db writing here
class Card(models.Model):
    front = models.CharField(max_length=256)
    back = models.CharField(max_length=512)
    image = models.ImageField(upload_to='card_images/', blank=True, null=True)
    
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='cards')
    
    def __str__(self):
        return f'front: {self.front} - back: {self.back}'
    
    def save(self, *args, **kwargs):
        # checks if a new card has been created
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            deck = self.deck
            # increases the related deck's card_count
            # 0-0: apparently "card_count += 1" should be avoided here because it could cause problems in cases 
            # where there are multiple concurrent requests and because it wouldn't apply to cards deleted through 
            # the admin interface.
            # 0-0: There is an even safer way of doing this which called F() expressions, but we gon worry about that when
            # we get a FANG job and not for shitty 0 user web apps.
            deck.card_count = deck.cards.count()
            # makes sure card_order is a dict
            if not deck.card_order:
                deck.card_order = {}
            # adds the card to the card_order
            if 'order' not in deck.card_order:
                deck.card_order = {'order': []}
            deck.card_order['order'].append(self.pk)
            
            # specifying which fields were updated optimizes db writing
            deck.save(update_fields=['card_count', 'card_order'])
    
    def delete(self):
        deck = self.deck
        card_pk = self.pk
        super().delete()
        
        # decreases related deck's card count
        deck.card_count = deck.cards.count()
        # makes sure card_order is a dict
        if not deck.card_order:
                deck.card_order = {}
        # removes the card from the deck's card_order
        if 'order' in deck.card_order and card_pk in deck.card_order['order']:
            deck.card_order['order'].remove(card_pk)
        
        deck.save(update_fields=['card_count', 'card_order'])
        

class Activity(models.Model):
    cards_reviewd = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='activity')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity')
    
    def __str__(self):
        return f'{self.user} reviewed {self.cards_reviewd} on {self.date}'