#coding=ISO-8859-1
from copy import copy
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.template.defaultfilters import slugify
from django.utils import timezone
from equipaments.models import Equipament, EquipamentType
from geoapi.models import Address
from medias.models import MusicianMedia

class MusicalStyle(models.Model):
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=255, null=True,blank = True)
    
    def __unicode__(self):
        return self.name

class MusicianSkill(models.Model):
    feeling = models.IntegerField(null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    versatility = models.IntegerField(null=True, blank=True)
    stage_performace = models.IntegerField(null=True, blank=True)
    commitment = models.IntegerField(null=True, blank=True)

class Musician(models.Model):
    url = models.SlugField(max_length=50)
    about = models.CharField(max_length=200)
    influences = models.CharField(max_length=150)

    born_year = models.IntegerField(null=True, blank=True)
    
    equipaments = models.ManyToManyField(Equipament)
    type_instruments_play = models.ManyToManyField(EquipamentType, null=True, blank=True)
    musical_styles = models.ManyToManyField(MusicalStyle, null=True, blank=True)
    
    media = models.OneToOneField(MusicianMedia, related_name="musician", null=True, blank=True)
    skills = models.OneToOneField(MusicianSkill, related_name="musician", null=True, blank=True)
    address = models.OneToOneField(Address, related_name="musician", null=True, blank=True)
    
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
    
    @property
    def profile_url(self):
        return "/musico/%s/%d" % (self.url, self.pk)
   
    def save(self, *args, **kwargs):
        self.url = slugify(self.name())

        if self.skills is None:
            self.skills = MusicianSkill.objects.create()

        if self.media is None:
            self.media = MusicianMedia.objects.create()

        if self.address is None:
            self.address = Address.objects.create()

        if self.address.city is None and self.address.state is None and self.address.cep != "":
            self.address.fill_by_cep()
            self.address.save()

        super(Musician, self).save(*args, **kwargs)
   
    def __unicode__(self):
        return self.name()

class Band(models.Model):
    about = models.CharField(max_length=1000)
    name = models.CharField(max_length=50)
    registration_date = models.DateTimeField('Registration date')
    musical_styles = models.ManyToManyField(MusicalStyle)
    url = models.SlugField(max_length=50)
    
    @property
    def musicians(self):
        return self.all_musicians.filter(active=True).all()
    
    @property
    def musicians_list(self):
        return [m.musician for m in self.musicians]
    
    def encode_page(self):
        return "/banda/%s/%d" % (self.url, self.pk)
    
    def is_admin(self, musician):
        return self.all_musicians.get(active=True, musician=musician).is_admin
    
    def add_musician(self, musician, instruments=None):
        if musician in self.musicians_list:
            raise ValueError("O musico %d ja esta na banda '%d'" %  (musician.id, self.id))
        
        musician_band = MusicianBand()
        musician_band.band = self
        musician_band.musician = musician
        musician_band.save()
        
        if instruments != None:
            musician_band.instruments = instruments
    
    def save(self, *args, **kwargs):
        self.url = slugify(self.name)
        if self.pk == None:
            self.registration_date = timezone.now()
        
        super(Band, self).save(*args, **kwargs)
        
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
        return  "%s na banda '%s'" % (self.musician.user.first_name, self.band.name)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Musician(user=instance).save()