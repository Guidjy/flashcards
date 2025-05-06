from django.urls import path
from . import views


urlpatterns = [
    path('', views.todos_usuarios),
    # registro, login e logout
    path('registrar/', views.registrar_usuario),
    path('login/', views.login_usuario),
    path('logout/', views.logout_usuario),
    # gerenciamento de decks
    path('criar_deck/', views.criar_deck),
    path('deletar_deck/<int:id>', views.deletar_deck),
    # gerenciamento de cards
    path('criar_card/', views.criar_card),
]