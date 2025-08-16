from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'decks', views.DeckViewSet)
router.register(r'cards', views.CardViewSet)

urlpatterns = [
    path('', views.test),
    path('', include(router.urls)),
]