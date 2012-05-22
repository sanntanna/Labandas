from bands.models import Musician, Band
from django.db import models

class SolicitationType(object):
    BAND,MUSICIAN = range(2)

class SolicitationStatus(object):
    PENDING,ACCEPTED,REJECTED = range(3)

class Solicitation(models.Model):
    from_musician = models.ForeignKey(Musician, related_name='solicitation_from')
    to_musician = models.ForeignKey(Musician, related_name='solicitation_to', Null=True)
    band = models.ForeignKey(Band)
    solicitation_type = models.IntegerField()
    solicitation_status = models.IntegerField()
    date = models.DateTimeField()
    active = models.BooleanField(default=True)