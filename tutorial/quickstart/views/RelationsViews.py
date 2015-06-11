__author__ = 'Administor'

from rest_framework import viewsets
from tutorial.quickstart.models import Relations
from tutorial.quickstart.serializers import RelationsSerializer
class RelationsView(viewsets.ModelViewSet):
    queryset = Relations.objects.all()
    serializer_class = RelationsSerializer
