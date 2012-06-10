#coding=ISO-8859-1
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
    def __generate_solicitation(self, from_musician=None, to_musician=None, band=None, instruments=None):
        return Solicitation(date=datetime.now(),
                            solicitation_status=Status.PENDING,
                            from_musician=from_musician,
                            to_musician=to_musician,
                            band=band)
     
    def ask_to_add(self, sender_musician, target_musician, band, instruments):
        if not band.musicians.get(musician=sender_musician).is_admin:
            raise SecurityError('Esse musico nao pode enviar solicitacao para essa banda')
        
        
        if target_musician.is_in_band(band):
            raise ValueError("O musico " + str(target_musician) + " ja pertence a banda " + str(band))
        
        solicitation = self.__generate_solicitation(from_musician=sender_musician, to_musician=target_musician, band=band)
        solicitation.solicitation_type = Type.ADD_TO_BAND
        solicitation.save()
        solicitation.instruments = instruments

        return True
    
    def bands_pending(self, musician):
        return musician.solicitation_to.filter(active=True, solicitation_type=Type.ADD_TO_BAND)
    
    def musicians_pending(self, band):
        return band.solicitations.filter(active=True, solicitation_type=Type.ADD_TO_BAND)
    
class Solicitation(models.Model):
    from_musician = models.ForeignKey(Musician, related_name='solicitation_from')
    to_musician = models.ForeignKey(Musician, related_name='solicitation_to')
    band = models.ForeignKey(Band, related_name='solicitations')
    instruments = models.ManyToManyField(EquipamentType)
    
    solicitation_type = models.IntegerField()
    solicitation_status = models.IntegerField()
    
    date = models.DateTimeField()
    active = models.BooleanField(default=True)

    objects = SolicitationManager()
    
    def accept(self, to_musician):
        if self.to_musician != to_musician:
            return False
        
        if self.solicitation_type == Type.ADD_TO_BAND:
            self.band.add_musician(self.to_musician, self.instruments.all())
        self.status = Status.ACCEPTED
        self.active = False
        
        self.save()
        
        return True
    
    def reject(self, to_musician):
        if self.to_musician != to_musician:
            return False
        
        self.status = Status.REJECTED
        self.active = False
        self.save()
        
        return True
    
    def cancel(self, from_musician):
        if not self.band.is_admin(from_musician):
            return False
        
        self.active = False
        self.save()
        
        return True
    
    def __unicode__(self):
        return self.from_musician.user.first_name + " convidou " + self.to_musician.user.first_name + " para a banda " + self.band.name
    
    
