from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.todos_usuarios),
    # registro, login e logout
    path('registrar/', views.registrar_usuario),
    path('login/', views.login_usuario),
    path('logout/', views.logout_usuario),
    # gerenciamento de decks
    path('criar_deck/', views.criar_deck),
    path('editar_deck/', views.editar_deck),
    path('deletar_deck/<int:id>', views.deletar_deck),
    path('get_deck/<int:id>', views.get_deck),
    # gerenciamento de cards
    path('criar_card/', views.criar_card),
    path('editar_card/', views.editar_card),
    path('deletar_card/<int:id>', views.deletar_card),
    path('get_card/<int:id>', views.get_card),
]