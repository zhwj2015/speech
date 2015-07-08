__author__ = 'Administor'

from rest_framework import viewsets
from tutorial.quickstart.models import Wavs, Users
from tutorial.quickstart.serializers import WavsSerializer
from rest_framework.response import Response
import os
from rest_framework.renderers import JSONRenderer
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from tutorial.quickstart.util import Util, JSONResponse
class WavsViews(viewsets.ModelViewSet):
    queryset = Wavs.objects.all()
    serializer_class = WavsSerializer

    def create(self, request, *args, **kwargs):
        try:
            pass
            # filename = request.data['wavs'].name
            # suffix=filename[filename.find('.'):]
            # name = Util.getTimestamp()
            # filename = str(name)+str(suffix)
            # path = 'wavs/'+filename
            # user_id = request.data['uid']
            # user = Users.objects.all().get(user_id=user_id)
            # created = request.data['created']
            # created = Util.strToTime(created,'%Y-%m-%d')
            #
            # if not os.path.exists('wavs/'):
            #     os.makedirs('wavs/')
            # out = open(path, 'wb+')
            # infile = request.data['wavs']
            # for chunk in infile.chunks():
            #     out.write(chunk)
            # out.flush()
            # out.close()
            # wav = Wavs(wav_id=name, name=filename, path=path, user_id=user, created=created, score=0)
            # serializer = WavsSerializer(wav)
            # json = JSONRenderer().render(serializer.data)
            # stream = BytesIO(json)
            # data = JSONParser().parse(stream)
            # serializer = WavsSerializer(data=data)
            # #object to JSON
            # # data = Util.serializeToJSON(serializer)
            # #
            # # serializer = WavsSerializer(data=data)
            # if serializer.is_valid():
            #     wav.save()
            # else:
            #     return JSONResponse({'status': False})
        except Exception, e:
            print "error"
            return JSONResponse({'status': False})
        return JSONResponse({'status': True})


