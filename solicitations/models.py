from bands.models import Musician, Band
from datetime import datetime
from django.db import models
from equipaments.models import EquipamentType
from twisted.test.test_pbfailure import SecurityError

class Type(object):
    RESPONSE_BAND_ANNOUNCEMENT, INVITE_TO_BAND, ADD_TO_BAND = range(3)

class Status(object):
    PENDING, ACCEPTED, REJECTED = range(3)

class SolicitationManager(models.Manager):

    def generate_solicitation(self, from_musician=None, to_musician=None, band=None, instruments=None):
        return Solicitation(date=datetime.now(),
                            solicitation_status=Status.PENDING,
                            from_musician=from_musician,
                            to_musician=to_musician,
                            band=band)
     
    def ask_to_add(self, sender_musician, target_musician, band, instruments):
        if not band.admins.filter(pk=sender_musician.pk):
            raise SecurityError('Esse musico nao pode enviar solicitacao para essa banda')
        
        
        if target_musician.is_in_band(band):
            raise ValueError("O musico " + str(target_musician) + " ja pertence a banda " + str(band))
        
        solicitation = self.generate_solicitation(from_musician=sender_musician, to_musician=target_musician, band=band)
        solicitation.solicitation_type = Type.ADD_TO_BAND
        solicitation.save()
        solicitation.instruments = instruments

        return True
    
    def band_pending(self, musician):
        return musician.solicitation_to.filter(active=True, solicitation_type=Type.ADD_TO_BAND)
    
    def accept(self, solicitation):
        if solicitation.solicitation_type == Type.ADD_TO_BAND:
            solicitation.band.add_musician(solicitation.to_musician, solicitation.instruments.all())
        
        solicitation.status = Status.ACCEPTED
        solicitation.active = False
        
        solicitation.save()
    
    def reject(self, solicitation):
        solicitation.status = Status.REJECTED
        solicitation.active = False
        solicitation.save()

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
    
    def __unicode__(self):
        return self.from_musician.user.first_name + " convidou " + self.to_musician.user.first_name + " para a banda " + self.band.name
    
    
