from bands.models import Musician, Band
from datetime import datetime
from django.db import models
from equipaments.models import EquipamentType

class Type(object):
    BAND, MUSICIAN = range(2)

class Status(object):
    PENDING, ACCEPTED, REJECTED = range(3)

class SolicitationManager(models.Manager):
    
    def generate_musician_solicitation(self, from_musician=None, to_musician=None, band=None, instruments=None):
        return Solicitation(date=datetime.now(), 
                            solicitation_status=Status.PENDING, 
                            from_musician=from_musician, 
                            to_musician=to_musician, 
                            instruments=instruments)
     
    def ask_musician(self, sender_musician, target_musician, band, instruments):
        
        if not band.admins.filter(pk=sender_musician.pk):
            return False
        
        solicitation = self.generate_new_solicitation(from_musician=sender_musician, to_musician=target_musician,band=band)
        solicitation.solicitation_type = Type.MUSICIAN
        solicitation.save()
        
        return True
    
    def ask_band(self, user, band):
        return None
        
    def list_pending_solicitations(self, user):
        return None

class Solicitation(models.Model):
    from_musician = models.ForeignKey(Musician, related_name='solicitation_from')
    to_musician = models.ForeignKey(Musician, related_name='solicitation_to')
    band = models.ForeignKey(Band)
    instruments = models.ManyToManyField(EquipamentType)
    
    solicitation_type = models.IntegerField()
    solicitation_status = models.IntegerField()
    date = models.DateTimeField()
    active = models.BooleanField(default=True)
    
    objects = SolicitationManager()
    
    
