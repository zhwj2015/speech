__author__ = 'Administor'
# -*- coding;utf-8 -*-
from rest_framework.decorators import detail_route
from tutorial.quickstart.models import Admin
from tutorial.quickstart.serializers import  AdminSerializer
from rest_framework import viewsets
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from tutorial.quickstart.util import Util

class JSONResponse(HttpResponse):
    '''
    An HttpResponse that renders its content into JSON
    '''
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


'''
    Admin View

'''
class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

    def create(self, request, *args, **kwargs):
        try:
            name = request.data['name']
            pwd = request.data['pwd']
            pwd = make_password(pwd, None, 'pbkdf2_sha256')
            user_id = Util.getTimestamp()
            admin = Admin(user_id = user_id, name = name, password =pwd)
            serializer = AdminSerializer(admin)
            data = Util.serializeToJSON(serializer)
            serializer = AdminSerializer(data=data)
            if serializer.is_valid():
                admin.save()
                return HttpResponse({"status": True})
        except Exception, e:
            return HttpResponse({"status": False})


    @detail_route(methods=['get'])
    def admin_list(self, request, pk=None):
        if request.method == "GET":
            pwd = request.GET['pwd']
            try:
                admin = Admin.objects.all().get(pk=pk)
                check_password(pwd, admin.password)
                serializer = AdminSerializer(admin)
                return JSONResponse(serializer.data)
            except Exception, e:
                return e


    @csrf_exempt
    @detail_route(methods=['post'])
    def reset_password(self, request, pk=None):
        admin = self.get_object()
        admin.set_password(request.data['password'])
        admin.save()
        return Response({'status': True})