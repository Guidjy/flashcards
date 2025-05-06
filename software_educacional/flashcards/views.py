from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import IntegrityError
from .models import User
from .serializers import UserSerializer


@api_view(['GET'])
def todos_usuarios(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def registrar_usuario(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'mensagem': 'Usuario registrado'})
    else:
        return Response({'mensagem': 'Usuario não registrado'})


@api_view(['POST'])
@csrf_exempt
def login_usuario(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    
    if user is not None:
        login(request, user)
        return Response({'mensagem': 'login realizado com sucesso', 'status': 200}, status=200)
    else:
        return Response({'error': 'Nome ou senha incorretos', 'status': 401}, status=401)