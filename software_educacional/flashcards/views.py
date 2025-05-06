from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import User, Deck, Card, Tag
from .serializers import UserSerializer, DeckSerializer, CardSerializer


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
    

@csrf_exempt
@api_view(['DELETE'])
def deletar_deck(request, id):  
    try:
        deck = Deck.objects.get(id=id)
    except Deck.DoesNotExist:
        return Response({'erro': 'Não foi encontrado um deck com esse id'}, status=401)
    
    deck.delete()
    return Response({'mensagem': 'Deck deletado com sucesso'}, status=200)


@csrf_exempt
@api_view(['POST'])
def criar_card(request):
    frente = request.data.get('frente')
    tras = request.data.get('tras')
    imagem = request.data.get('imagem')
    
    try:
        deck = Deck.objects.get(nome=request.data.get('deck'))
    except Deck.DoesNotExist:
        return Response({'erro': 'Não existe um deck com esse nome'}, status=401)
    
    tag = request.data.get('tag')
    try:
        tag = Tag.objects.get(nome=tag)
    except Tag.DoesNotExist:
        tag = Tag.objects.create(nome=request.data.get('tag'))
        try:
            tag.full_clean()
        except ValidatioError:
            tag = None
            
    novo_card = Card.objects.create(frente=frente, tras=tras, imagem=imagem, deck=deck, tag=tag)
    try:
        novo_card.full_clean()
    except ValidationError:
        return Response({'erro': 'Credenciais de card inválidos'}, status=400)
    else:
        deck.numero_de_cards += 1
        deck.save()
        return Response({'mensagem': 'Card criado com sucesso', 'card': CardSerializer(novo_card).data}, status=200)
    
    
@csrf_exempt
@api_view(['DELETE'])
def deletar_card(request, id):  
    try:
        card = Card.objects.get(id=id)
    except Card.DoesNotExist:
        return Response({'erro': 'Não foi encontrado um card com esse id'}, status=401)
    
    deck_do_card = Deck.objects.get(id=card.deck.id)
    deck_do_card.numero_de_cards -= 1
    deck_do_card.save()
    
    card.delete()
    return Response({'mensagem': 'card deletado com sucesso'}, status=200)
    