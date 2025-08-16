from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

router = DefaultRouter()
router.register(r'', views.UserViewSet)

urlpatterns = [
    # register
    path('register/', views.register),
    # login (jwt authentication)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # user CRUD operations
    path('users/', include(router.urls)),
    path('me/', views.get_current_user),
]