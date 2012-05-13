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
    
    cep = models.CharField(max_length=9, null=True,blank = True)
    city = models.CharField(max_length=20, null=True,blank = True)
    state = models.CharField(max_length=2, null=True,blank = True)
    latitute = models.FloatField(null=True,blank = True)
    longitude = models.FloatField(null=True,blank = True)
    
    user = models.OneToOneField(User)
    
    def __unicode__(self):
        return self.user.first_name
    
    def get_musician_bands(self):
        return MusicianBand.objects.filter(musician=self)

class Band(models.Model):
    name = models.CharField(max_length=50)
    registration_date = models.DateTimeField('Registration date')
    musical_styles = models.ManyToManyField(MusicalStyle)
    medias = models.ManyToManyField(Media)
    admins = models.ManyToManyField(Musician)
        
    def __unicode__(self):
        return self.name
    
    def save_adding_musician(self, musician, instruments):
        self.save()
        musicianBand = MusicianBand()
        musicianBand.band = self
        musicianBand.musician = musician
        musicianBand.save()
        musicianBand.instruments = instruments
    
class MusicianBand(models.Model):
    band = models.ForeignKey(Band)
    musician = models.ForeignKey(Musician)
    instruments = models.ManyToManyField(EquipamentType)
    
    def __unicode__(self):
        return self.musician.user.first_name + ' na banda "' + self.band.name + '"'

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Musician.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)