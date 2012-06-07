#coding=ISO-8859-1
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch.dispatcher import receiver
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
    
    def name(self):
        return self.user.get_full_name()
    
    @property
    def bands(self):
        return self.all_bands.filter(musician=self, active=True).all()
    
    @property
    def bands_list(self):
        return [b.band for b in self.bands] 
    
    def is_in_band(self, band):
        return MusicianBand.objects.filter(musician=self, band=band, active=True).exists()
    
    def set_cep(self, cep=None):
        if cep == None:
            return
        self.cep = cep
    
    def encode_profile(self):
        return "/musico/" + self.url + "/" + self.pk.__str__()
   
    def __unicode__(self):
        return self.name()
   
    @classmethod
    def pre_save(sender, instance, created, **kwargs):
        instance._generate_url_() 

class Band(models.Model):
    name = models.CharField(max_length=50)
    registration_date = models.DateTimeField('Registration date')
    musical_styles = models.ManyToManyField(MusicalStyle)
    medias = models.ManyToManyField(Media)
    url = models.SlugField(max_length=50)
    
    @property
    def musicians(self):
        return self.all_musicians.filter(active=True).all()
    
    @property
    def musicians_list(self):
        return [m.musician for m in  self.musicians]
    
    def encode_page(self):
        return "/banda/" + self.url + "/" + str(self.pk)
    
    def save(self, *args, **kwargs):
        self.url = slugify(self.name)
        super(Band, self).save(*args, **kwargs)
    
    def is_admin(self, musician):
        return self.all_musicians.get(active=True, musician=musician).is_admin
    
    def add_musician(self, musician, instruments=None):
        if musician in self.musicians_list:
            raise ValueError("O musico %d ja esta na banda %d" %  (musician.id, self.id))
        
        musician_band = MusicianBand()
        musician_band.band = self
        musician_band.musician = musician
        musician_band.save()
        
        if instruments != None:
            musician_band.instruments = instruments
    
    def __unicode__(self):
        return self.name
    
class MusicianBand(models.Model):
    band = models.ForeignKey(Band, related_name="all_musicians")
    musician = models.ForeignKey(Musician, related_name="all_bands")
    instruments = models.ManyToManyField(EquipamentType)
    active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    def deactivate(self):
        self.active = False
        self.save()
        return True
        
    def __unicode__(self):
        return self.musician.user.first_name + ' na banda "' + self.band.name + '"'

@receiver(pre_save, sender=Musician)
def pre_save_musician(sender, instance, **kwargs):
    instance.url = slugify(instance.name())

@receiver(pre_save, sender=Band)
def pre_save_band(sender, instance, **kwargs):
    if instance.pk == None:
        instance.registration_date = datetime.now()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Musician(user=instance).save()