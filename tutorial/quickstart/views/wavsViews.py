__author__ = 'Administor'

from rest_framework import viewsets
from tutorial.quickstart.models import Wavs, Users
from tutorial.quickstart.serializers import WavsSerializer
from rest_framework.response import Response
import time
import os
from tutorial.quickstart.util import Util
class WavsViews(viewsets.ModelViewSet):
    queryset = Wavs.objects.all()
    serializer_class = WavsSerializer

    def create(self, request, *args, **kwargs):
        filename = request.data['wavs'].name
        suffix=filename[filename.find('.'):]
        name = Util.getTimestamp()
        filename = str(name)+str(suffix)
        path = 'wavs/'+filename
        user_id = request.data['uid']
        user = Users.objects.all().get(user_id=user_id)
        try:
            if not os.path.exists('wavs/'):
                os.makedirs('wavs/')
            out = open(path, 'wb+')
            infile = request.data['wavs']
            for chunk in infile.chunks():
                out.write(chunk)
            out.flush()
            out.close()
            wav = Wavs(wav_id=name, name=filename, path=path, user_id=user, score=70)
            serializer = WavsSerializer(wav)
            #object to JSON
            data = Util.serializeToJSON(serializer)

            serializer = WavsSerializer(data=data)
            if serializer.is_valid():
                wav.save()

        except Exception, e:
            print "error"
            return Response({'status': False})
        return Response({'status': True})


