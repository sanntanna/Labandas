from bands.models import Musician
from django.db import models

class SolicitationType(object):
    BAND,MUSICIAN = range(2)

class SolicitationStatus(object):
    PENDING,ACCEPTED,REJECTED = range(3)

class Solicitation(models.Model):
    from_musician = models.ForeignKey(Musician, related_name='solicitation_from_musician')
    to_musician = models.ForeignKey(Musician, related_name='solicitation_to_musician')
    date = models.DateTimeField()
    solicitation_type = models.IntegerField()
    solicitation_status = models.IntegerField()
    active = models.BooleanField(default=True)