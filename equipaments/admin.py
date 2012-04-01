from django.db import models
from equipaments.models import Equipament

# Create your models here.

class MusicalStyle(models.Model):
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=255, null=True,blank = True)
    def __unicode__(self):
        return self.name

class Musician(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    equipaments = models.ManyToManyField(Equipament)
    musical_styles = models.ManyToManyField(MusicalStyle)
    def __unicode__(self):
        return self.name

class Band(models.Model):
    name = models.CharField(max_length=50)
    musicians = models.ManyToManyField(Musician)
    registration_date = models.DateTimeField('Registration date')
    musical_styles = models.ManyToManyField(MusicalStyle)
    def __unicode__(self):
        return self.name