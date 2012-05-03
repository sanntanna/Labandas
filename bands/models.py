from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from equipaments.models import Equipament

class MusicalStyle(models.Model):
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=255, null=True,blank = True)
    def __unicode__(self):
        return self.name

class MusicianType(models.Model):
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=255, null=True,blank = True)
    def __unicode__(self):
        return self.name

class Musician(models.Model):
    equipaments = models.ManyToManyField(Equipament)
    musician_type = models.ManyToManyField(MusicianType)
    musical_styles = models.ManyToManyField(MusicalStyle)
    account = models.OneToOneField(User)
    
    def __unicode__(self):
        return self.account.first_name + " " + self.account.last_name

class Band(models.Model):
    name = models.CharField(max_length=50)
    musicians = models.ManyToManyField(Musician)
    registration_date = models.DateTimeField('Registration date')
    musical_styles = models.ManyToManyField(MusicalStyle)
    def __unicode__(self):
        return self.name


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Musician.objects.create(account=instance)

post_save.connect(create_user_profile, sender=User)