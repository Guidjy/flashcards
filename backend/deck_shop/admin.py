from django.contrib import admin
from .models import Tag, Listing, ListingImage, Reaction


admin.site.register(Tag)
admin.site.register(Listing)
admin.site.register(ListingImage)
admin.site.register(Reaction)
