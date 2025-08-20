from django.contrib import admin
from .models import Tag, Listing, ListingImage


admin.site.register(Tag)
admin.site.register(Listing)
admin.site.register(ListingImage)
