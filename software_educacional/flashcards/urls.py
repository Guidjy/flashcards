from django.urls import path
from . import views


urlpatterns = [
    path('', views.todos_usuarios),
    path('registrar_usuario', views.registrar_usuario),
    path('login_usuario', views.login_usuario),
]