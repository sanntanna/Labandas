from bands.models import Band, Musician
from django.db import models
from equipaments.models import EquipamentType

class Announcement(models.Model):
    owner_band = models.ForeignKey(Band)
    instruments = models.ManyToManyField(EquipamentType)
    text = models.CharField(max_length=140, null=True,blank = True)
    active = models.BooleanField(default=True)
    musicians_candidates = models.ManyToManyField(Musician, related_name="announcements")