from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'tags', views.TagViewSet)
router.register(r'listings', views.ListingViewSet)
router.register(r'listing-images', views.ListingImageViewSet)
router.register(r'reactions', views.ReactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]