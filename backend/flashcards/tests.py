from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Deck, Card, Activity 

"""
O ciclo de vida de um teste segue este padrão:
1) Setup de Classe: O banco é preparado.
2) setUp(): Cria os objetos iniciais (ex: um Deck e um User).
3) Execução: O método test_algo() roda.
4) Asserções (assertions): Você verifica se o resultado é o esperado usando self.assertEqual, self.assertTrue, etc.
5) TearDown: O Django limpa o que foi feito no banco.
"""


User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        # Cria um usuário de teste inicial para os métodos desta classe
        self.user = User.objects.create_user(username='usuario_teste', password='senha_forte_123')

    def test_user_creation(self):
        """Verifica se o usuário foi criado corretamente com os atributos básicos."""
        self.assertEqual(self.user.username, 'usuario_teste')
        self.assertTrue(self.user.is_active)

    def test_user_str_method(self):
        """Verifica se a representação em string do usuário retorna o username."""
        self.assertEqual(str(self.user), 'usuario_teste')


class DeckModelTest(TestCase):
    def setUp(self):
        # Cria dependências necessárias para testar o Deck
        self.user = User.objects.create_user(username='dono_deck', password='password123')
        self.deck = Deck.objects.create(name='Python Básico', owned_by=self.user)

    def test_deck_creation(self):
        """Verifica se o Deck é instanciado com os valores padrão corretos."""
        self.assertEqual(self.deck.name, 'Python Básico')
        self.assertEqual(self.deck.card_count, 0)
        # Verifica se o JSONField inicia como um dicionário vazio
        self.assertEqual(self.deck.card_order, {}) 
        self.assertEqual(self.deck.owned_by, self.user)

    def test_deck_str_method(self):
        """Verifica se o método __str__ do Deck retorna apenas o seu nome."""
        self.assertEqual(str(self.deck), 'Python Básico')


class CardModelTest(TestCase):
    def setUp(self):
        # Configuração de ambiente para os testes de Card
        self.user = User.objects.create_user(username='dono_card', password='password123')
        self.deck = Deck.objects.create(name='Django Avançado', owned_by=self.user)

    def test_card_creation_updates_deck_count_and_order(self):
        """Verifica se ao criar um Card, o Deck relacionado atualiza o contador e a lista de ordem."""
        card1 = Card.objects.create(front='O que é QuerySet?', back='Uma coleção de consultas ao DB.', deck=self.deck)
        
        # IMPORTANTE: Precisamos dar um refresh_from_db pois o Deck foi alterado 
        # por um processo paralelo no save() do Card.
        self.deck.refresh_from_db()
        
        self.assertEqual(self.deck.card_count, 1)
        self.assertIn('order', self.deck.card_order)
        self.assertEqual(self.deck.card_order['order'], [card1.pk])

    def test_multiple_cards_maintain_correct_order(self):
        """Garante que múltiplos cartões são adicionados sequencialmente na lista de ordem do Deck."""
        card1 = Card.objects.create(front='Q1', back='A1', deck=self.deck)
        card2 = Card.objects.create(front='Q2', back='A2', deck=self.deck)
        card3 = Card.objects.create(front='Q3', back='A3', deck=self.deck)
        
        self.deck.refresh_from_db()
        self.assertEqual(self.deck.card_count, 3)
        # A ordem deve seguir a criação: [ID1, ID2, ID3]
        self.assertEqual(self.deck.card_order['order'], [card1.pk, card2.pk, card3.pk])

    def test_updating_existing_card_does_not_duplicate_order(self):
        """Garante que editar um card existente não altere o contador ou a lista de ordem."""
        card = Card.objects.create(front='Pergunta Original', back='Resposta', deck=self.deck)
        
        # Atualiza o card (isso aciona o save(), mas is_new será False)
        card.front = 'Pergunta Editada'
        card.save()
        
        self.deck.refresh_from_db()
        self.assertEqual(self.deck.card_count, 1) # Não deve subir para 2
        self.assertEqual(len(self.deck.card_order['order']), 1) # Não deve duplicar a PK na lista

    def test_card_deletion_updates_deck_count_and_order(self):
        """Verifica se ao deletar um Card, ele é removido do contador e da lista de ordem do Deck."""
        card1 = Card.objects.create(front='Q1', back='A1', deck=self.deck)
        card2 = Card.objects.create(front='Q2', back='A2', deck=self.deck)
        
        self.deck.refresh_from_db()
        self.assertEqual(self.deck.card_count, 2)
        
        card1_pk = card1.pk
        card1.delete()
        
        self.deck.refresh_from_db()
        self.assertEqual(self.deck.card_count, 1)
        # O ID do card deletado não deve mais estar na lista de ordem
        self.assertNotIn(card1_pk, self.deck.card_order['order'])
        self.assertEqual(self.deck.card_order['order'], [card2.pk])

    def test_card_str_method(self):
        """Verifica a formatação da string de representação do Card."""
        card = Card.objects.create(front='Frente', back='Verso', deck=self.deck)
        self.assertEqual(str(card), 'front: Frente - back: Verso')


class ActivityModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='estudante', password='password123')
        self.deck = Deck.objects.create(name='Vocabulário', owned_by=self.user)
        self.activity = Activity.objects.create(
            cards_reviewd=20,
            correct_answers=15,
            deck=self.deck,
            user=self.user
        )

    def test_activity_creation(self):
        """Verifica se os dados de atividade foram gravados e se a data foi gerada automaticamente."""
        self.assertEqual(self.activity.cards_reviewd, 20)
        self.assertEqual(self.activity.correct_answers, 15)
        self.assertEqual(self.activity.deck, self.deck)
        self.assertEqual(self.activity.user, self.user)
        # auto_now_add deve definir a data de hoje
        self.assertEqual(self.activity.date, timezone.now().date())

    def test_activity_str_method(self):
        """Verifica se o log de atividade exibe as informações legíveis corretamente."""
        data_hoje = self.activity.date
        expected_str = f'estudante reviewed 20 on {data_hoje}'
        self.assertEqual(str(self.activity), expected_str)
        
"""
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
Testes de integração
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class FlashcardAPITest(APITestCase):
    def setUp(self):
        # 1. Criação de usuário para autenticação
        self.user = User.objects.create_user(username='api_user', password='password123')
        
        # Força a autenticação do cliente de teste (Pula a necessidade de passar tokens manualmente)
        self.client.force_authenticate(user=self.user)
        
        # 2. Criação de dados iniciais para testar endpoints de leitura (GET)
        self.deck = Deck.objects.create(name='Deck de Teste API', owned_by=self.user)
        self.card1 = Card.objects.create(front='Frente 1', back='Verso 1', deck=self.deck)
        self.card2 = Card.objects.create(front='Frente 2', back='Verso 2', deck=self.deck)

    def test_create_deck_via_api(self):
        """Testa se o endpoint de ViewSet consegue criar um Deck e associá-Flow banco."""
        url = '/decks/' # Caso tenha usado reverse: reverse('deck-list')
        data = {'name': 'Novo Deck API', 'owned_by': self.user.id}
        
        response = self.client.post(url, data)
        
        # Verifica se a requisição foi um sucesso (201 Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verifica se o deck foi realmente salvo no banco de dados
        self.assertTrue(Deck.objects.filter(name='Novo Deck API').exists())

    def test_create_card_via_api_updates_deck(self):
        """
        O TESTE DE INTEGRAÇÃO DEFINITIVO:
        Garante que a View da API aciona corretamente as regras de negócio do Modelo (card_count).
        """
        url = '/cards/'
        data = {
            'front': 'Nova Pergunta',
            'back': 'Nova Resposta',
            'deck': self.deck.id
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Atualiza o deck do banco para ver se o CardViewSet triggou o save() do modelo corretamente
        self.deck.refresh_from_db()
        self.assertEqual(self.deck.card_count, 3) # 2 criados no setUp + 1 criado agora via API

    def test_get_user_decks_endpoint(self):
        """Testa a custom route /get-user-decks"""
        url = '/get-user-decks'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assumindo que a view retorna uma lista de decks, verificamos se nosso deck está lá
        # O formato exato depende de como você configurou sua view, mas o teste básico de status garante a conectividade.
        self.assertIn('Deck de Teste API', str(response.data))

    def test_take_test_endpoint(self):
        """Testa a custom route /take-test/<int:deck_id>/<int:n_questions>"""
        # Simulando o usuário pedindo 2 questões do deck criado
        url = f'/take-test/{self.deck.id}/2'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Como é um teste de integração, podemos garantir que os dados vieram (ex: 2 itens na lista de resposta)
        # Ajuste a asserção abaixo de acordo com o formato (JSON) que a sua view devolve
        if isinstance(response.data, list):
            self.assertTrue(len(response.data) <= 2)

    def test_view_deck_stats_endpoint(self):
        """Testa a custom route /view-deck-stats/<int:deck_id>"""
        # Primeiro, criamos uma atividade para ter estatísticas para mostrar
        Activity.objects.create(
            cards_reviewd=10, 
            correct_answers=8, 
            deck=self.deck, 
            user=self.user
        )
        
        url = f'/view-deck-stats/{self.deck.id}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_unauthenticated_user_cannot_create_deck(self):
        """Garante que rotas protegidas não podem ser acessadas sem login."""
        # Desloga o usuário de teste
        self.client.force_authenticate(user=None)
        
        url = '/decks/'
        data = {'name': 'Deck Ilegal'}
        response = self.client.post(url, data)
        
        # O status deve ser 401 Unauthorized ou 403 Forbidden
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.assertFalse(Deck.objects.filter(name='Deck Ilegal').exists())