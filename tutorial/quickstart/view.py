__author__ = 'Administor'
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tutorial.quickstart.models import Snippet
from tutorial.quickstart.serializers import SnippetSerializer

@api_view(['GET','POST'])
def snippet_list(request):
    '''
    List all snippet, or create a new snippet
    '''
    if request.method == "GET":
        snippets  = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

