# -*- coding:utf-8 -*-


from django.contrib.auth.models import User, Group
from django.db.models import Q
from rest_framework import viewsets
from tutorial.quickstart.serializers import UserSerializer, GroupSerializer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from tutorial.quickstart.models import Snippet
from tutorial.quickstart.serializers import SnippetSerializer

from rest_framework.decorators import detail_route
from tutorial.quickstart.models import Users, Admin, Keymodels, Keywords, Relations, Positions
from tutorial.quickstart.serializers import UsersSerializer, AdminSerializer, KeymodelsSerializer, KeywordsSerializer, RelationsSerializer, PositionsSerializer
from django.contrib.auth.hashers import make_password, check_password
from django.template.context_processors import csrf
from tutorial.quickstart.util import Util, JSONResponse

from django.http.response import HttpResponseRedirect
from  datetime import *


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

'''
    logic
'''


from django.shortcuts import render, render_to_response

'''
controller
'''

'''
    redirect to index.html
'''

def index(request):
    return render(request, 'index.html')

'''
    redict to main.html
'''
def main(request):
    try:
        username = request.session['uid']
        c = {'username': username}
        c.update(csrf(request))
        return render_to_response('main.html', c)
    except Exception,e:
        return HttpResponseRedirect('/index')


'''
    获取职工信息，通过关键字获取还有分页
    param: page->分页查询时使用,表示当前页码,keyword->搜索用户时使用,表示搜索关键字
    :return JSONResponse Users and Positions
'''
def user(request):
    try:
        try:
            username = request.session['uid']
            if username == None:
                return HttpResponseRedirect({'redirect':'/index'})
        except Exception,e:
            return JSONResponse({'redirect':'/index'})
        data =  dict(request.GET)
        page = 1
        keyword = ''
        num = 10
        if data.has_key('page'):
            page = int(data.get('page')[0])
        if data.has_key('keyword'):
            keyword = str(data.get('keyword')[0])
        users = Users.objects.filter(Q(user_id__icontains = keyword) | Q(name__icontains = keyword) | Q(position__name__icontains=keyword)).order_by('add_time').reverse()
        if users.count() % num == 0:
            pageNum = int(users.count() / num)
        else:
            pageNum = int(users.count() / num) + 1

        if pageNum == 0:
            pageNum = 1
        users = users[(page-1)*num:(page)*num]
        positions = Positions.objects.all()
        #print users.user_id
        object_all = list(users) + list(positions)
        #the set of users
        ss = UsersSerializer(users, many=True)
        #the set of positions
        ps = PositionsSerializer(positions, many=True)
        sJson = Util.serializeToJSON(ss)
        pJson = Util.serializeToJSON(ps)
        return JSONResponse({'Users': sJson, 'Positions': pJson, 'pageNum': pageNum, 'curPage':page})
    except Exception,e:
        return JSONResponse({'False':False})

def getUserById(request):
    try:
        user_id = request.GET['user_id']
        user = Users.objects.filter(Q(user_id__icontains=user_id))
        userSerialize = UsersSerializer(user, many=True)
        userJson = Util.serializeToJSON(userSerialize)
        return JSONResponse({'user':userJson})
    except Exception, e:
        pass

'''
    update the User
    :return if the update is fail return False and if the update is success return User object
'''
def update(request):
    try:
        data = request.POST
        data = dict(data.iterlists())
        user_id = data.get('data[user_id]')[0]
        name = data.get('data[name]')[0]
        sex = data.get('data[sex]')[0]
        age = data.get('data[age]')[0]
        birthday = Util.strToTime(str(data.get('data[birthday]')[0]), '%Y-%m-%d')
        position = Positions.objects.all().get(pid=data.get('data[position][pid]')[0])
        score = data.get('data[score]')[0]
        rows = Users.objects.filter(user_id=user_id).update(user_id=user_id, name=name,sex=sex, age=age, birthday=birthday, position=position, score=score)
        if rows > 0:
            user = Users.objects.all().get(user_id = user_id)
            serializer = UsersSerializer(user)
            return JSONResponse(Util.serializeToJSON(serializer))
        else:
            return JSONResponse({"False": False})
    except Exception, e:
        return JSONResponse({"False":False})

'''
    添加用户信息
'''
def add(request):
    try:
        data = request.POST
        data = dict(data.iterlists())
        name = data.get('data[name]')[0]
        sex = data.get('data[sex]')[0]
        age = data.get('data[age]')[0]
        birthday = Util.strToTime(str(data.get('data[birthday]')[0]), '%Y-%m-%d')
        position = Positions.objects.all().get(pid=data.get('data[position][pid]')[0])
        score = data.get('data[score]')[0]
        user_id = str(Util.getTimestamp())
        add_time = datetime.now()
        user = Users(user_id=user_id, name=name,sex=sex, age=age, birthday=birthday, position=position, score=score,add_time=add_time)
        user.save()
        serializer = UsersSerializer(user)
        return JSONResponse(Util.serializeToJSON(serializer))
    except Exception, e:
        return JSONResponse({'False': False})


'''
    删除多条用户信息
    :returns 如果用户信息删除成功，返回多用户id，如果失败，恢复用户信息，返回False
'''
def delete(request):
    try:
        data = request.GET
        data = dict(data)
        ids = data.get('ids[]')
        users = []
        for user_id in ids:
            user = Users.objects.all().get(user_id=user_id)
            users.append(user)
            Users.objects.filter(user_id= user_id).delete()
        return JSONResponse(ids)
    except Exception, e:
        for user in users:
            user.save()
        return JSONResponse({'False': False})


'''
    通过关键字搜索用户信息
    :returns type JSON 用户信息
'''

def search(request):
    try:
        keyword =  request.GET.get('keyword')
        page = 1
        num = 10
        users = Users.objects.filter(Q(user_id__icontains = keyword) | Q(name__icontains = keyword) | Q(position__name__icontains=keyword)).order_by('add_time').reverse()
        if users.count() % num == 0:
            pageNum = int(users.count() / num)
        else:
            pageNum = int(users.count() / num) + 1
        if pageNum == 0:
            pageNum = 1
        users = users[(page-1)*num:(page)*num]
        serializers = UsersSerializer(users, many=True)
        json_user = Util.serializeToJSON(serializers)
        # json_return = JSONRenderer().render({'users':json_user,'curPage': page,'total':pageNum})
        return JSONResponse({'users':json_user,'curPage': page,'total':pageNum,'keyword':keyword})
    except Exception, e:
        return JSONResponse({"False": False})
# class Users11z():
#     def user(request):
#         users = Users.objects.all()
#         #print users.user_id
#         print users.count()
#         print serializers.serialize('json', users)
#         return HttpResponse(serializers.serialize('json', users,use_natural_primary_keys=True))
#         #return render(request, 'user.html', {'users': users, 'count': users.count()})
#     @csrf_exempt
#     def update(request):
#         user_id = request.POST['user_id']
#         user = User.objects.all().get(user_id=user_id).update(request.data)
#         return HttpResponse(True)


'''
    login to system

'''
@csrf_exempt
def login(request):
    username = request.POST['username']
    pwd = request.POST['password']
    try:
        admin = Admin.objects.all().get(name=username)
        blnPwd = check_password(pwd, admin.password)
        if blnPwd:
            request.session['uid'] = username
            return HttpResponseRedirect("/main")
        else:
            return render(request, 'index.html', {'error_msg': '用户名或密码错误'})
    except Exception,e:
        return render(request, 'index.html', {'error_msg': '用户名或密码错误'})
'''
    log out
'''
def logout(request):
    try:
        del request.session['uid']
        return HttpResponseRedirect('/index')
    except KeyError:
        return HttpResponseRedirect('/index')


def sign(request):
    username = request.GET['uid']
    pwd = request.GET['pwd']
    try:
        admin = Admin.objects.all().get(name=username)
        blnPwd = check_password(admin.password, pwd)
    except Exception,e:
        return HttpResponse(e)


def testUpload(request):
    return render_to_response('testupload.html')