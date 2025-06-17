from django.contrib.auth import authenticate, login, logout

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import User, Deck, Card, Tag
from .serializers import UserSerializer, DeckSerializer, CardSerializer

from google import genai
import json
import re


# usuários


@api_view(['POST'])
@permission_classes([AllowAny])
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
    

@api_view(['PATCH'])
def editar_usuario(request):
    usuario = request.user
    novo_nome = request.data.get('novoNome')
    nova_senha = request.data.get('novaSenha')
    novo_email = request.data.get('novoEmail')
    nova_imagem = request.data.get('novaImagem')
    
    if novo_nome:
        usuario.username = novo_nome
    if nova_senha:
        usuario.password = nova_senha
    if novo_email:
        usuario.email = novo_email
    if nova_imagem:
        usuario.imagem_de_perfil = nova_imagem
        
    usuario.save()
    
    return Response({'mensagem': 'usuario editado com sucesso', 'usuario': UserSerializer(usuario).data})
    

@api_view(['POST'])
@permission_classes([AllowAny])
def login_usuario(request):
    nome = request.data.get('nome')
    senha = request.data.get('senha')
    print(nome)
    print(senha)

    usuario = authenticate(request, username=nome, password=senha)
    print(usuario)

    if usuario is not None:
        login(request, usuario)
        return Response({'messagem': 'Login realizado com sucesso.'})
    else:
        return Response({'erro': 'Credenciais invalidos'}, status=401)


@api_view(['GET'])
def logout_usuario(request):
    logout(request)
    return Response({'messagem': 'Logout realizado com sucesso.'})


@api_view(['GET'])
def perfil_usuario(request):
    usuario = UserSerializer(request.user)
    return Response(usuario.data)


@api_view(['GET'])
def todos_usuarios(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


# Deck


@api_view(['POST'])
def criar_deck(request):
    nome = request.data.get('nome')
    criador = request.user
    novo_deck = Deck.objects.create(nome=nome, criador=criador)
    
    try:
        novo_deck.full_clean()
    except ValidationError:
        return Response({'erro': 'Campos do deck inválidos'}, status=401)
    else:
        return Response({'deckCriado': DeckSerializer(novo_deck).data})


@api_view(['PATCH'])
def editar_deck(request):
    deck = request.data.get('id')
    novo_nome = request.data.get('novoNome')
    
    try:
        deck = Deck.objects.get(id=deck)
    except Deck.DoesNotExist:
        return Response({'erro': 'Não foi encontrado um deck com esse id'}, status=401)
    else:
        deck.nome = novo_nome
        deck.save()
        return Response({'mensagem': 'Deck editado com sucesso'}, status=200)
    
    
@api_view(['DELETE'])
def deletar_deck(request, id):  
    try:
        deck = Deck.objects.get(id=id)
    except Deck.DoesNotExist:
        return Response({'erro': 'Não foi encontrado um deck com esse id'}, status=401)
    
    deck.delete()
    return Response({'mensagem': 'Deck deletado com sucesso'}, status=200)


@api_view(['GET'])
def get_deck(request, id):
    try:
        deck = Deck.objects.get(id=id)
    except Deck.DoesNotExist:
        return Response({'erro': 'Não foi encontrado um deck com esse id'}, status=401)
    
    cards_do_deck = Card.objects.filter(deck=deck)
    cards_do_deck = CardSerializer(cards_do_deck, many=True).data
    deck = DeckSerializer(deck).data
    
    return Response({'deck': deck, 'cardsDoDeck': cards_do_deck}, status=200)


@api_view(['GET'])
def decks_usuario(request):
    usuario = request.user
    decks_do_usuario = Deck.objects.filter(criador=usuario.id)
    serializer = DeckSerializer(decks_do_usuario, many=True)
    
    return Response(serializer.data)


# Card


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
        except ValidationError:
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
    

@api_view(['PATCH'])
def editar_card(request):
    card = request.data.get('id')
    nova_frente = request.data.get('novaFrente')
    nova_tras = request.data.get('novaTras')
    nova_imagem = request.data.get('novaImagem')
    nova_tag = request.data.get('novaTag')
    
    try:
        card = Card.objects.get(id=card)
    except Card.DoesNotExist:
        return Response({'erro': 'Não existe um card com esse id'}, status=400)
    
    if nova_frente:
        card.frente = nova_frente
    if nova_tras:
        card.tras = nova_tras
    if nova_imagem:
        card.imagem = nova_imagem
    if nova_tag:
        try:
            nova_tag = Tag.objects.get(nome=nova_tag)
        except Tag.DoesNotExist:
            nova_tag = Tag.objects.create(nome=nova_tag)
            try:
                nova_tag.full_clean()
            except ValidationError:
                nova_tag = None
        finally:
            card.tag = nova_tag
            
    card.save()
    return Response({'mensagem': 'Card editado com sucesso', 'card': CardSerializer(card).data}, status=200)
        

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
    

@api_view(['GET'])
def get_card(request, id):
    try:
        card = Card.objects.get(id=id)
    except Card.DoesNotExist:
        return Response({'erro': 'Não foi encontrado um card com esse id'}, status=401)

    card = CardSerializer(card).data
    return Response({'card': card})


# Estudo


@api_view(['GET'])
def comecar_estudo(request, id):
    try:
        deck = Deck.objects.get(id=id)
    except Deck.DoesNotExist:
        return Response ({'erro': 'Não existe um deck com esse id'})
        
    cards = Card.objects.filter(deck=deck)
    
    if len(deck.ordem_dos_cards['ordem']) == 0:
        for card in cards:
            deck.ordem_dos_cards['ordem'].append(card.id)
        deck.save()
    
    ordem = deck.ordem_dos_cards['ordem']
    cards_ordenados = sorted(cards, key=lambda card: ordem.index(card.id))
    
    return Response(CardSerializer(cards_ordenados, many=True).data)


@api_view(['PATCH'])
def terminar_estudo(request):
    try:
        deck = Deck.objects.get(id=request.data.get('id'))
    except Deck.DoesNotExist:
        return Response ({'erro': 'Não existe um deck com esse id'})
    
    nova_ordem = request.data.get('novaOrdem')
    deck.ordem_dos_cards['ordem'] = nova_ordem
    deck.save()
    
    return Response({'mensagem': 'estudo encerrado com sucesso'})


# pesquisa de decks


@api_view(['GET'])
@permission_classes([AllowAny])
def todos_decks(request):
    decks = Deck.objects.all().order_by('-likes')
    serializer = DeckSerializer(decks, many=True)
    
    return Response(serializer.data)


@api_view(['GET'])
def pesquisar_por_nome(request, nome):
    # peep the query
    decks = Deck.objects.filter(nome_icontains=nome).order_by('-likes')
    serializer = DeckSerializer(decks, many=True)
    
    return Response(serializer.data)
    


# AI

@api_view(['GET'])
def teste_ai(request):
    client = genai.Client(api_key=":p")
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        contents="Explique brevemente como IA funciona."
    )
    return Response({'response': response.text})


@api_view(['GET'])
def criar_teste(request, deck_id, n_questoes):
    """
    Cria n_questoes com base no deck de deck_id
    """
    try:
        deck = Deck.objects.get(id=deck_id)
    except Deck.DoesNotExist:
        return Response({'erro': f'Não existe um deck com o id {deck_id}'}, status=400)
    
    cards_do_deck = Card.objects.filter(deck=deck)
    card_serializer = CardSerializer(cards_do_deck, many=True)
    
    client = genai.Client(api_key=":p")
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        contents=f"Crie {n_questoes} questões de múltipla escolha, com 4 alternativas, com base no conteúdo dos seguintes flashcards, e me retorne-as em uma lista de json com os campos \"pergunta\", \"a\", \"b\", \"c\", \"d\" e \"Resposta\". flashcards: {card_serializer.data}"
    )
    
    # converte resposta da prompt para json
    lista_json = re.search(r'\[.*\]', response.text, re.DOTALL)

    if lista_json:
        texto_json = lista_json.group(0)
        data = json.loads(texto_json)
    else:
        return Response({'erro': 'Erro na geração do teste.'}, status=400)
    
    return Response({'questões': data}, status=200)

