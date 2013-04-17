from bands.models import Band, Musician
from django.db import models
from equipaments.models import EquipamentType

class Announcement(models.Model):
    owner_band = models.ForeignKey(Band, related_name="announcements")
    instruments = models.ManyToManyField(EquipamentType)
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=140)
    active = models.BooleanField(default=True)
    musicians_candidates = models.ManyToManyField(Musician, related_name="announcements", blank=True)
    
    def __unicode__(self):
        return self.owner_band.name + " - " + self.text[0:20] + "..."