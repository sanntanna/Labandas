#coding=ISO-8859-1
from django.db import models
from django.template.defaultfilters import slugify

class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=255, null=True, blank=True)
    def __unicode__(self):
        return self.name
    
class EquipamentType(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category)

    @property
    def normalized_name(self):
        return slugify(self.name)

    def __unicode__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=50)
    logo = models.CharField(max_length=255, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    def __unicode__(self):
        return self.name
    
class Equipament(models.Model):
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=255, null=True, blank=True)
    brand = models.ForeignKey(Brand)
    equipament_type = models.ForeignKey(EquipamentType)
    def __unicode__(self):
        return self.equipament_type.name + " " + self.brand.name + " " + self.name