__author__ = 'Administor'
from rest_framework import viewsets
from tutorial.quickstart.models import Keymodels
from tutorial.quickstart.serializers import KeywordsSerializer
class KmViews(viewsets.ModelViewSet):
    queryset = Keymodels.objects.all()
    serializer_class = KeywordsSerializer
