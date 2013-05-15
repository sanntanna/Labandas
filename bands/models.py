#coding=UTF-8
from copy import copy
from django.contrib.auth.models import User
from networkconnect.models import UserNetwork
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.template.defaultfilters import slugify
from django.utils import timezone
from equipaments.models import Equipament, EquipamentType
from geoapi.models import Address
from medias.models import MusicianMedia, BandMedia

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
        
    @property
    def photos_url(self):
        return "/musico/%s/%d/fotos" % (self.url, self.pk)

    @property
    def videos_url(self):
        return "/musico/%s/%d/videos" % (self.url, self.pk)

    @property
    def bands_url(self):
        return "/musico/%s/%d/bandas" % (self.url, self.pk)
   
    def save(self, *args, **kwargs):
        self.url = slugify(self.name())

        if self.skills is None:
            self.skills = MusicianSkill.objects.create()

        if self.media is None:
            self.media = MusicianMedia.objects.create()

        if self.address is None:
            self.address = Address.objects.create()

        if not self.address.cep is None and self.address.cep != "":
            self.address.fill_by_cep()
            self.address.save()

        super(Musician, self).save(*args, **kwargs)
   
    def __unicode__(self):
        return self.name()


class Band(models.Model):
    about = models.CharField(max_length=1000)
    name = models.CharField(max_length=50)
    influences = models.CharField(max_length=150)
    registration_date = models.DateTimeField('Registration date')

    musical_styles = models.ManyToManyField(MusicalStyle)
    
    url = models.SlugField(max_length=50)

    media = models.OneToOneField(BandMedia, related_name="band", null=True, blank=True)
    
    @property
    def musicians(self):
        return self.all_musicians.filter(active=True).all()
    
    @property
    def musicians_list(self):
        return [m.musician for m in self.musicians]

    @property
    def admin(self):
        return self.all_musicians.filter(is_admin=True).all()[0].musician
    
    @property
    def page_url(self):
        return "/banda/%s/%d" % (self.url, self.pk)
    
    @property
    def setlist_url(self):
        return "/banda/%s/%d/setlist" % (self.url, self.pk)

    @property
    def photos_url(self):
        return "/banda/%s/%d/fotos" % (self.url, self.pk)

    @property
    def videos_url(self):
        return "/banda/%s/%d/videos" % (self.url, self.pk)

    @property
    def history_ads(self):
        return "/banda/%s/%d/historico-de-anuncios" % (self.url, self.pk)

    def is_admin(self, musician):
        return self.all_musicians.get(active=True, musician=musician).is_admin
    
    def add_musician(self, musician, instruments=None, is_admin=False):
        if musician in self.musicians_list:
            raise ValueError("O musico %d ja esta na banda '%d'" %  (musician.id, self.id))
        
        musician_band = MusicianBand()
        musician_band.band = self
        musician_band.musician = musician
        musician_band.is_admin = is_admin
        musician_band.save()
        
        if instruments != None:
            musician_band.instruments = instruments
    
    def add_music_to_setlist(self, music):
        if isinstance(music, basestring):
            return SetlistMusic.objects.create(band=self, title=music)
        
        musics = []
        for m in music:
            musics.append(SetlistMusic.objects.create(band=self, title=m))

        return musics

    def save(self, *args, **kwargs):
        self.url = slugify(self.name)
        if self.pk == None:
            self.registration_date = timezone.now()

            if self.media is None:
                self.media = BandMedia.objects.create()

        super(Band, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.name


class SetlistMusicManager(models.Manager):
    def create(self, *args, **kwargs):
        title = kwargs['title'].rstrip().rstrip('\r\n')
        band = kwargs['band']

        if title == '' or self.filter(title=title, band=band):
            return

        return super(SetlistMusicManager, self).create(*args, **kwargs)

class SetlistMusic(models.Model):
    band = models.ForeignKey(Band, related_name="setlist")
    title = models.CharField(max_length=150)
    url = models.CharField(max_length=150, null=True, blank=True)
    registration_date = models.DateTimeField('Registration date')

    objects = SetlistMusicManager()

    def save(self, *args, **kwargs):
        if self.pk == None:
            self.registration_date = timezone.now()
        
        super(SetlistMusic, self).save(*args, **kwargs)

    def exists(self, band, title):
        return self.objects.filter(band = band, title = title).count() > 0

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-registration_date']

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


@receiver(post_save, sender=UserNetwork)
def handle_network_data(sender, instance, created, **kwargs):
    musician = instance.user.get_profile()
    changed = False

    if 'birthday' in instance.extra_fields:
        musician.born_year = instance.extra_fields['birthday'].split('/')[2]
        changed = True

    if 'avatar_url' in instance.extra_fields:
        import urllib, cStringIO

        avatar_image = cStringIO.StringIO(urllib.urlopen(instance.extra_fields['avatar_url']).read())
        musician.media.avatar = avatar_image
        changed = True

    if changed:
        musician.save()
    