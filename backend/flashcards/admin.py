from django.contrib import admin
from .models import Deck, Card, Activity, AccountabilityPartner


admin.site.register(Deck)
admin.site.register(Card)
admin.site.register(Activity)
admin.site.register(AccountabilityPartner)
