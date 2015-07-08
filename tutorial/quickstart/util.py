__author__ = 'Administor'
# -*- coding:utf-8 -*-
import datetime
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
import time
from django.http import HttpResponse

class Util():

    '''
     usage: str to datetime using format, format '%Y-%m-%d'
    '''
    @staticmethod
    def strToTime(str, format):
        return datetime.datetime.strptime(str, format)


    '''
    useage: wav = Wav(param)
            serializer = WavSerializer(wav)
            data = serializerToJSON(serializer)
            serializer = WavSerializser(data=data)
            if serializer.is_valid():
                wav.save()
            "object to serializer" to use SERIALIZER's method is_valid() to valid the object
    '''

    @staticmethod
    def serializeToJSON(serializer):
        content = JSONRenderer().render(serializer.data)
        stream = BytesIO(content)
        data = JSONParser().parse(stream)
        return data

    '''
    time to timestamp
    '''
    @staticmethod
    def getTimestamp():
        return int(time.time())

    # @staticmethod
    # def modelToSerializer(model):
    #     return  serializers.serialize('json', model, use_natural_foreign_keys=True, use_natural_primary_keys=False)


class JSONResponse(HttpResponse):
    '''
    An HttpResponse that renders its content into JSON
    '''
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)