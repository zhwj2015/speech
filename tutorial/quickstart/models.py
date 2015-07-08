from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

# Create your models here.

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ('created',)

class Admin(models.Model):
    user_id = models.CharField(max_length=20)
    name=models.CharField(max_length=250)
    password = models.CharField(max_length=250)

    def set_password(self, pwd):
        self.password = pwd
    def get_password(self):
        return self.password

class PositionsManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

class Positions(models.Model):
    objects = PositionsManager()
    pid = models.CharField(max_length=20,primary_key=True)
    name = models.CharField(max_length=100)
    condition = models.TextField()

    def natural_key(self):
        return (self.name)
    # class Meta:
    #     unique_together = (('name'))
    class Meta:
        unique_together = (( 'name'),)
    def __unicode__(self):
        return self.pid

class Users(models.Model):
    user_id = models.CharField(max_length=20)
    name = models.CharField(max_length=250)
    sex = models.IntegerField()
    age = models.IntegerField()
    birthday = models.DateTimeField()
    position = models.ForeignKey('Positions')
    score = models.IntegerField()
    add_time =  models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('add_time',)



class Wavs(models.Model):
    wav_id = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    path = models.CharField(max_length=500)
    created = models.DateTimeField()
    user_id = models.ForeignKey('Users')
    score = models.IntegerField(12)

    class Meta:
        ordering = ('created',)


class Keywords(models.Model):
    word_id = models.CharField(max_length=20, primary_key=True)
    keyword = models.CharField(max_length=250)
    model_id = models.ForeignKey('Keymodels')
    plus = models.BooleanField()

class Keymodels(models.Model):
    model_id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)

class Relations(models.Model):
    model_id = models.ForeignKey("Keymodels")
    word_id = models.ForeignKey("Keywords")
    user_id = models.ForeignKey("Users")
    wav_id = models.ForeignKey("Wavs")
    count = models.IntegerField()