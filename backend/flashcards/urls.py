from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'decks', views.DeckViewSet)
router.register(r'cards', views.CardViewSet)
router.register(r'activities', views.ActivityViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('get-user-decks', views.get_user_decks),
    path('take-test/<int:deck_id>/<int:n_questions>', views.take_test),
    path('view-deck-stats/<int:deck_id>', views.view_deck_stats),
]