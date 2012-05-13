from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from equipaments.models import Equipament, EquipamentType
from medias.models import Media

class MusicalStyle(models.Model):
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=255, null=True,blank = True)
    def __unicode__(self):
        return self.name

class Musician(models.Model):
    equipaments = models.ManyToManyField(Equipament)
    type_instruments_play = models.ManyToManyField(EquipamentType)
    musical_styles = models.ManyToManyField(MusicalStyle)
    medias = models.ManyToManyField(Media)
    user = models.OneToOneField(User)
    
    def __unicode__(self):
        return self.user.first_name

class Band(models.Model):
    name = models.CharField(max_length=50)
    registration_date = models.DateTimeField('Registration date')
    musical_styles = models.ManyToManyField(MusicalStyle)
    medias = models.ManyToManyField(Media)
    admins = models.ManyToManyField(Musician)
        
    def __unicode__(self):
        return self.name

class MusicianBand(models.Model):
    band = models.ForeignKey(Band)
    musician = models.ForeignKey(Musician)
    instrument = models.ForeignKey(EquipamentType)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Musician.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)