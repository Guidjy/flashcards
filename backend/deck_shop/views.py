# rest framework
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
# objects
from .models import *
from .serializers import *


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    
    # enables filtering and ordering (django-filter module)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['tags__name']           # filters listings by tags
    ordering_fields = ['created_at', 'likes']   # allowed ordering fields
    ordering = ['-created_at']                  # default ordering
    

class ListingImageViewSet(viewsets.ModelViewSet):
    queryset = ListingImage.objects.all()
    serializer_class = ListingImageSerializer
    

class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
    

    

