from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.forms import widgets
from models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES, Admin, Users, Keymodels, Keywords, Relations, Wavs, Positions

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

'''
class SnippetSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):

        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)

        instance.save()
        return instance
'''

class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        field = ('id', 'title', 'code', 'linenos', 'language', 'style')

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        field = ('id','user_id','name','password')
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        field = (
            'id',
            'user_id',
            'name',
            'sex',
            'age',
            'birthday',
            'position',
            'score',
        )
        depth = 1
class KeywordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keywords
        field = (
            'word_id',
            'keyword',
            'plus',
        )
class KeymodelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keymodels
        field = (
            'model_id',
            'name',
            'created',
        )
class RelationsSerializer(serializers.ModelSerializer):
    model_id = serializers.PrimaryKeyRelatedField(queryset=Keymodels.objects.all())
    word_id = serializers.PrimaryKeyRelatedField(queryset=Keywords.objects.all())
    user_id = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    wav_id = serializers.PrimaryKeyRelatedField(queryset=Wavs.objects.all())
    class Meta:
        model = Relations
        field = (
            'model_id ',
            'word_id',
            'user_id',
            'wav_id',
            'count',
        )

class WavsSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Wavs
        field = (
            'id',
            'wav_id',
            'name',
            'path',
            'created',
            'user_id',
            'score',
        )

class PositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Positions
        field = (
            'pid',
            'name',
            'condition',
        )