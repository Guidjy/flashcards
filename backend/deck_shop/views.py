from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def test(request):
    return Response({'yurp': 'deck-shop routed'}, status=200)
