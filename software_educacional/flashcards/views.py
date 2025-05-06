from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import User, Deck
from .serializers import UserSerializer, DeckSerializer


@csrf_exempt
@api_view(['POST'])
def registrar_usuario(request):
    nome = request.data.get('nome')
    senha = request.data.get('senha')
    confirmacao_senha = request.data.get('confirmacaoSenha')
    email = request.data.get('email')
    imagem = request.data.get('imagemDePerfil', None)

    if not nome or not senha:
        return Response({'erro': 'Nome e senha são obrigatórios.'}, status=400)
    
    if senha != confirmacao_senha:
        return Response({'erro': 'Senha e confirmação da senha devem ser iguais'}, status=400)

    try:
        user = User.objects.create_user(username=nome, password=senha, email=email)
        if imagem:
            user.imagem_de_perfil = imagem
            user.save()
        return Response({'messagem': 'Usuário criado com sucesso.'}, status=201)
    except Exception as e:
        return Response({'erro': str(e)}, status=400)
    

@csrf_exempt
@api_view(['POST'])
def login_usuario(request):
    nome = request.data.get('nome')
    senha = request.data.get('senha')

    usuario = authenticate(request, username=nome, password=senha)

    if usuario is not None:
        login(request, usuario)
        return Response({'messagem': 'Login realizado com sucesso.'})
    else:
        return Response({'erro': 'Credenciais invalidos'}, status=401)


@csrf_exempt
@api_view(['POST'])
def logout_usuario(request):
    logout(request)
    return Response({'messagem': 'Logout realizado com sucesso.'})


@api_view(['GET'])
def todos_usuarios(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
def criar_deck(request):
    nome = request.data.get('nome')
    criador = request.user
    novo_deck = Deck.objects.create(nome=nome, criador=criador)
    
    try:
        novo_deck.full_clean()
    except ValidatioError:
        return Response({'erro': 'Campos do deck inválidos'}, status=401)
    else:
        return Response({'deckCriado': DeckSerializer(novo_deck).data})
    