from django.core.exceptions import ValidationError
from django.db import IntegrityError

from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from email_validator import validate_email, EmailNotValidError

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    | Method | Endpoint          | Action         |
    | ------ | ----------------- | -------------- |
    | GET    | `/users/`         | List users     |
    | POST   | `/users/`         | Create user    |
    | GET    | `/users/{id}/`    | Retrieve user  |
    | PUT    | `/users/{id}/`    | Full update    |
    | PATCH  | `/users/{id}/`    | Partial update |
    | DELETE | `/users/{id}/`    | Delete user    |
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Creates a new user.
    ### body:
    {
        "username": string,
        "email": string,
        "password": string,
        "passwordConfirmation": string
    }
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')
    
    if not username or not email or not password or not password_confirmation:
        return Response({'error': 'All fields are required.'}, status=400)
    
    try:
        email_info = validate_email(email, check_deliverability=True)
    except EmailNotValidError as e:
        return Response({'error': f'{e}'}, status=400)
    
    if password != password_confirmation:
        return Response({'error': 'Password and password confirmation do not match.'}, status=400)
    
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
            )
        user.full_clean()
        user.save()
    except ValidationError as e:
        return Response({'error': e.message_dict}, status=400)
    except IntegrityError:
        return Response({'error': 'Username or email already in use.'}, status=400)
    
    serializer = UserSerializer(user)
    
    return Response({'success': 'User successfully created.', 'user': serializer.data}, status=200)


@api_view(['GET'])
def get_current_user(request):
    """
    Returns data about the currently authenticated user
    """
    user = request.user
    return Response(UserSerializer(user).data)