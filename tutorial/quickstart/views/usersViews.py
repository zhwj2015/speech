__author__ = 'Administor'


from rest_framework.decorators import detail_route
from tutorial.quickstart.models import Users
from tutorial.quickstart.serializers import UsersSerializer
from rest_framework import viewsets
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from tutorial.quickstart.models import Positions

from tutorial.quickstart import util


class UsersViewsSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def create(self, request, *args, **kwargs):
        request.data['birthday'] = util.Util.strToTime(str(request.data['birthday']), '%Y-%m-%d')
        request.data['position'] = Positions.objects.all().get(name=request.data['position'])
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': True})
        else:
            return Response({'status': False})

    @csrf_exempt
    @detail_route(methods=['post'])
    def update_user(self, request, pk=None):
        user = self.get_object()
        for field in UsersSerializer.Meta.field:
            print field
            if request.data.has_key(field):
                setattr(user, field, request.data[field])
        user.save()
        return Response({'status': True})
