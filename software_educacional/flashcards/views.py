from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def teste(request):
    person = {'name': 'Guilherme', 'age': 19}
    return Response(person)
