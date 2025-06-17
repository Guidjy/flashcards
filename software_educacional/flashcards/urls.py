from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', views.todos_usuarios),
    # registro, login e logout
    path('registrar/', views.registrar_usuario),
    path('editar_usuario/', views.editar_usuario),
    # authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('perfil/', views.perfil_usuario),
    # gerenciamento de decks
    path('criar_deck/', views.criar_deck),
    path('editar_deck/', views.editar_deck),
    path('deletar_deck/<int:id>', views.deletar_deck),
    path('get_deck/<int:id>', views.get_deck),
    path('decks_usuario/', views.decks_usuario),
    path('todos_decks/', views.todos_decks),
    # gerenciamento de cards
    path('criar_card/', views.criar_card),
    path('editar_card/', views.editar_card),
    path('deletar_card/<int:id>', views.deletar_card),
    path('get_card/<int:id>', views.get_card),
    # realização de estudo
    path('comecar_estudo/<int:id>', views.comecar_estudo),
    path('terminar_estudo/', views.terminar_estudo),
    # pesquisa de decks
    # AI
    path('teste_ai/', views.teste_ai),
    path('criar_teste/<int:deck_id>/<int:n_questoes>/', views.criar_teste),
]