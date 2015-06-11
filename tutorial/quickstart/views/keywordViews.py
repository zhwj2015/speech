__author__ = 'Administor'

from rest_framework.decorators import detail_route
from tutorial.quickstart.models import Keywords
from tutorial.quickstart.serializers import  KeywordsSerializer
from rest_framework import viewsets
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

class KeywordViews(viewsets.ModelViewSet):
    queryset = Keywords
    serializer_class = KeywordsSerializer
