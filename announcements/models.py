#coding=ISO-8859-1
from bands.models import Band, Musician
from django.db import models
from django.utils import timezone
from equipaments.models import EquipamentType
from solicitations.models import Solicitation
from labandas.helpers import EmailSender

class Announcement(models.Model):
    instruments = models.ManyToManyField(EquipamentType)
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=600)
    active = models.BooleanField(default=True)
    registration_date = models.DateTimeField('Registration date')

    owner_band = models.ForeignKey(Band, related_name="announcements")
    candidates = models.ManyToManyField(Musician, related_name="announcements", blank=True)

    def save(self, *args, **kwargs):
        if self.pk == None:
            self.registration_date = timezone.now()

        super(Announcement, self).save(*args, **kwargs)

    def add_candidate(self, musician):
        if not self.active:
            raise ValueError("O anúncio %d está inativo" % self.id)

        if musician in self.candidates.all():
            return False

        self.candidates.add(musician)
        solicitation = Solicitation.objects.reply_announcement(musician, self.owner_band)
        EmailSender.announcement_reply(solicitation, self)

        return True
    
    def __unicode__(self):
        return self.owner_band.name + " - " + self.text[0:20] + "..."