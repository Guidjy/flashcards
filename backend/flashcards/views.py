# rest framework
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
# objects
from .models import Deck, Card, Activity, AccountabilityPartner
from .serializers import DeckSerializer, CardSerializer, ActivitySerializer, AccountabilityPartnerSerializer
# libraries
import os
from google import genai
from .utils import extract_json_from_string


class DeckViewSet(viewsets.ModelViewSet):
    queryset = Deck.objects.all()
    serializer_class = DeckSerializer
    

class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    

class AccountabilityPartnerViewSet(viewsets.ModelViewSet):
    queryset = AccountabilityPartner.objects.all()
    serializer_class = AccountabilityPartnerSerializer


@api_view(['GET'])
def take_test(request, deck_id, n_questions):
    """
    Generates a multiple choice test with "n_questions" based on the contents of
    the cards of "deck_id".
    """
    # queries db for deck
    try:
        deck = Deck.objects.get(id=deck_id)
    except Deck.DoesNotExist:
        return Response({'error': f'Deck with id {deck_id} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # gets cards from that deck
    cards = deck.cards.all()
    cards = CardSerializer(cards, many=True).data
        
    # makes request to the google gemini api
    api_key = os.getenv('GENAI_API_KEY')
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f'Based on the contents of the following flashcards, create a multiple choice test with {n_questions} questions, with each question having 4 choices, and return them in a json list in the following format:' + '{"question": <question>, "A": <choice A>, "B": <choice B>, "C": <choice C>, "D": <choice D>, "answer": <A, B, C or D>}' + f'flashcards: {cards}'
    )
    questions = extract_json_from_string(response.text)

    return Response({'test': questions}, status=status.HTTP_200_OK)


@api_view(['GET'])
def view_deck_stats(request, deck_id):
    """
    Generates a graph that shows the number of correct answers when reviewing a deck over time.
    """
    # queries db for deck
    try:
        deck = Deck.objects.get(id=deck_id)
    except Deck.DoesNotExist:
        return Response({'error': f'Deck with id {deck_id} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # gets all activity related to that deck
    activity = Activity.objects.filter(deck=deck)
    if (len(activity) == 0):
        return Response({'warning': 'No activity found for this deck.'}, status=status.HTTP_200_OK)
    
    activity = ActivitySerializer(activity, many=True)
    print(activity)
    
    return Response({'stats': activity.data})
    
    