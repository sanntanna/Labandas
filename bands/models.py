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
        return MusicianBand.objects.filter(musician=self, active=True)
    
    def get_bands(self):
        return self.get_musician_bands().values('band__id', 'band__name')
    
    def is_in_band(self, band):
        return MusicianBand.objects.filter(musician=self, band=band, active=True).exists()
    
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
    url = models.SlugField(max_length=50)
        
    def __unicode__(self):
        return self.name
    
    def encode_page(self):
        return "/banda/" + self.url + "/" + self.pk.__str__()
    
    def save(self, *args, **kwargs):
        self.url = slugify(self.name)
        super(Band, self).save(*args, **kwargs)
    
    def musicians_active(self):
        return self.musicians.filter(active=True)
    
    def add_musician(self, musician, instruments):
        musician_band = MusicianBand()
        musician_band.band = self
        musician_band.musician = musician
        musician_band.save()
        musician_band.instruments = instruments
    
class MusicianBand(models.Model):
    band = models.ForeignKey(Band, related_name="musicians")
    musician = models.ForeignKey(Musician, related_name="bands")
    instruments = models.ManyToManyField(EquipamentType)
    active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    def deactivate(self):
        self.active = False
        self.save()
        return True
        
    def __unicode__(self):
        return self.musician.user.first_name + ' na banda "' + self.band.name + '"'

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Musician(user=instance).save()

post_save.connect(create_user_profile, sender=User)