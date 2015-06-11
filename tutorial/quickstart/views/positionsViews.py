__author__ = 'Administor'

from rest_framework import viewsets
from tutorial.quickstart.models import Positions
from tutorial.quickstart.serializers import PositionsSerializer

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Positions.objects.all()
    serializer_class = PositionsSerializer
