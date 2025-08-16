from rest_framework import serializers
from .models import User


# used for making CRUD operations on user models
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_picture', 'first_name', 'last_name', 'is_staff', 'is_active']
        read_only_fields = ['id', 'is_staff', 'is_active']