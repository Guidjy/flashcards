from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.todos_usuarios),
    # registro, login e logout
    path('registrar/', views.registrar_usuario),
    path('login/', views.login_usuario),
    path('editar_usuario/<int:usuario_id>/', views.editar_usuario),
    path('perfil/<int:usuario_id>/', views.perfil_usuario),
    # gerenciamento de decks
    path('criar_deck/', views.criar_deck),
    path('editar_deck/', views.editar_deck),
    path('deletar_deck/<int:deck_id>', views.deletar_deck),
    path('get_deck/<int:deck_id>', views.get_deck),
    path('decks_usuario/<int:usuario_id>', views.decks_usuario),
    path('todos_decks/', views.todos_decks),
    # gerenciamento de cards
    path('criar_card/', views.criar_card),
    path('editar_card/', views.editar_card),
    path('deletar_card/<int:card_id>', views.deletar_card),
    path('get_card/<int:card_id>', views.get_card),
    # realização de estudo
    path('comecar_estudo/<int:deck_id>', views.comecar_estudo),
    path('terminar_estudo/', views.terminar_estudo),
    # AI
    path('teste_ai/', views.teste_ai),
    path('criar_teste/<int:deck_id>/<int:n_questoes>/', views.criar_teste),
]