from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
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
    url = models.SlugField(max_length=50)
    
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
    
    def get_bands(self):
        return self.get_musician_bands().values('band__id', 'band__name')
    
    def set_cep(self, cep=None):
        if cep == None:
            return
        self.cep = cep
    
    def encode_profile(self):
        return "/musico/" + self.url + "/" + self.pk.__str__()
    
    def save(self, *args, **kwargs):
        self.url = slugify(self.user.first_name)
        super(Musician, self).save(*args, **kwargs)

class Band(models.Model):
    name = models.CharField(max_length=50)
    registration_date = models.DateTimeField('Registration date')
    musical_styles = models.ManyToManyField(MusicalStyle)
    medias = models.ManyToManyField(Media)
    admins = models.ManyToManyField(Musician)
    url = models.SlugField(max_length=50)
        
    def __unicode__(self):
        return self.name
    
    def encode_page(self):
        return "/banda/" + self.url + "/" + self.pk.__str__()
    
    def save(self, *args, **kwargs):
        self.url = slugify(self.name)
        super(Band, self).save(*args, **kwargs)
    
    def get_musicians(self):
        return MusicianBand.objects.filter(band=self)
    
    def add_musician(self, musician, instruments):
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
        Musician(user=instance).save()

post_save.connect(create_user_profile, sender=User)