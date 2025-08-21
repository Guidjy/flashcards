from django.conf import settings
# rest framework
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
# objects
from .models import Deck, Card, Activity, AccountabilityPartner
from .serializers import DeckSerializer, CardSerializer, ActivitySerializer, AccountabilityPartnerSerializer
# libraries
import os
import datetime
from google import genai
import matplotlib.pyplot as plt
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
    Generates a graph that shows the number of correct answers when reviewing a deck over the current month.
    """
    # queries db for deck
    try:
        deck = Deck.objects.get(id=deck_id)
    except Deck.DoesNotExist:
        return Response({'error': f'Deck with id {deck_id} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # gets all activity related to that deck
    today = datetime.date.today()
    activities = Activity.objects.filter(
        deck=deck, 
        date__year=today.year, 
        date__month=today.month
    ).order_by('date')
    
    # checks if there's enough data to plot a graph
    if (len(activities) == 0):
        return Response({'warning': 'No activity found for this deck this month.'}, status=status.HTTP_200_OK)
    if (len(activities) == 1):
        return Response({'warning' 'Deck has only been reviewed once this month. Try again after reviewing another day.'}, status=status.HTTP_200_OK)
    
    # gets plot data
    graph_axes = {'dates': [], 'correct_answers': []}
    for activity in activities:
        graph_axes['dates'].append(activity.date.day)
        graph_axes['correct_answers'].append(activity.correct_answers)
        
    # plots the graph
    fig, ax = plt.subplots()
    ax.plot(graph_axes['dates'], graph_axes['correct_answers'], color='blue')       
    ax.set_xlabel("Date")
    ax.set_ylabel("Correct Answers")
    
    # saves graph to disk
    save_dir = os.path.join(settings.MEDIA_ROOT, 'stat_graphs')
    os.makedirs(save_dir, exist_ok=True)  # creates dir if it doesn't exist
    file_path = os.path.join(save_dir, f'deck_stats{deck_id}.png')
    fig.savefig(file_path, format='png')
    plt.close(fig)
    
    file_url = os.path.join(settings.MEDIA_URL, 'stat_graphs', f'deck_stats{deck_id}.png')
    file_url = os.getenv('BACKEND_DOMAIN') + file_url
    
    return Response({'stats': file_url})


@api_view(['GET'])
def view_friend_activity(request):
    """
    Gets number of cards reviewd by all of the current user's accountability partners.
    """
    #TODO
    