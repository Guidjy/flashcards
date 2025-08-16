# rest framework
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
# objects
from .models import Deck, Card
from .serializers import DeckSerializer, CardSerializer


@api_view(['GET'])
def test(request):
    return Response({'Success': 'api working'}, status=status.HTTP_200_OK)


class DeckViewSet(viewsets.ModelViewSet):
    queryset = Deck.objects.all()
    serializer_class = DeckSerializer
    

class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer