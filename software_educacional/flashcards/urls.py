from django.urls import path
from . import views


urlpatterns = [
    path('', views.todos_usuarios),
    path('registrar/', views.registrar_usuario),
    path('login/', views.login_usuario),
    path('logout/', views.logout_usuario),
]