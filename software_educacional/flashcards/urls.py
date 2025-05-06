from django.urls import path
from . import views


urlpatterns = [
    path('', views.todos_usuarios),
    path('registrar/', views.registrar_usuario),
    path('login/', views.login_usuario),
    path('logout/', views.logout_usuario),
    path('criar_deck/', views.criar_deck),
    path('deletar_deck/', views.deletar_deck),
]