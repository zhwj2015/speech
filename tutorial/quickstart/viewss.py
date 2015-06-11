# -*- coding:utf-8 -*-


from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from tutorial.quickstart.serializers import UserSerializer, GroupSerializer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from tutorial.quickstart.models import Snippet
from tutorial.quickstart.serializers import SnippetSerializer

from rest_framework.decorators import detail_route
from tutorial.quickstart.models import Users, Admin, Keymodels, Keywords, Relations
from tutorial.quickstart.serializers import UsersSerializer, AdminSerializer, KeymodelsSerializer, KeywordsSerializer, RelationsSerializer
from django.contrib.auth.hashers import make_password, check_password

from django.http.response import HttpResponseRedirect
class JSONResponse(HttpResponse):
    '''
    An HttpResponse that renders its content into JSON
    '''
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@csrf_exempt
def snippet_list(request, format=None):
    '''
    List all code snippet, or create a new snippet
    '''
    if request.method == "GET":
        snippet = Snippet.objects.all()
        serializer = SnippetSerializer(snippet, many=True)
        return JSONResponse(serializer.data)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def snippet_detail(request, pk, format=None):
    '''
    retrieve, update or delete a code snippet
    '''
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExit:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = SnippetSerializer(snippet)
        return JSONResponse(serializer.data)
    elif request.method == "PUT":
        data = JSONParser().pase(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)
    elif request.method == "DELETE":
        snippet.delete()
        return HttpResponse(status=204)

@csrf_exempt
def Users_list(request, format=None):
    if request.method == "GET":
        users = Users.objects.all()
        serializers = UsersSerializer(users, many=True)
        return JSONResponse(serializers.data)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = UsersSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
@detail_route(methods=['get'])
def Admin_list(request, format=None):
    if request.method == "GET":
        users = Admin.objects.all()
        serializers = AdminSerializer(users, many=True)
        return JSONResponse(serializers.data)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        print data
        serializer = AdminSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


from django.shortcuts import render
'''
controller
'''
def index(request):
    return render(request, 'index.html',{'result': 'test'})
    
def main(request):
    username = request.session['uid']
    return render(request, 'main.html', {'username': username})

@csrf_exempt
def login(request):
    username = request.POST['username']
    pwd = request.POST['password']
    try:
        admin = Admin.objects.all().get(name=username)
        blnPwd = check_password(pwd, admin.password)
        if blnPwd:
            request.session['uid'] = username
            print request.session['uid']
            return HttpResponseRedirect("/main")
        else:
            return render(request, 'index.html', {'error_msg': '用户名或密码错误'})
    except Exception,e:
        return render(request, 'index.html', {'error_msg': '用户名或密码错误'})

def logout(request):
    try:
        del request.session['uid']
    except KeyError:
        pass


def sign(request):
    username = request.GET['uid']
    pwd = request.GET['pwd']
    try:
        admin = Admin.objects.all().get(name=username)
        blnPwd = check_password(admin.password, pwd)
    except Exception,e:
        return HttpResponse(e)