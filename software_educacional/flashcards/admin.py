from django.contrib import admin
from .models import User, Deck, Tag, Card, Like


admin.site.register(User)
admin.site.register(Deck)
admin.site.register(Tag)
admin.site.register(Card)
admin.site.register(Like)
