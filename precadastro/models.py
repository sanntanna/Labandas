#coding=ISO-8859-1
from django.db import models

class Record(models.Model):

	UFS = (
		('AC', 'Acre'),
		('AL', 'Alagoas'),
		('AP', 'Amapá'),
		('AM', 'Amazonas'),
		('BA', 'Bahia '),
		('CE', 'Ceará'),
		('DF', 'Distrito Federal'),
		('ES', 'Espírito Santo'),
		('GO', 'Goiás'),
		('MA', 'Maranhão'),
		('MT', 'Mato Grosso'),
		('MS', 'Mato Grosso do Sul'),
		('MG', 'Minas Gerais'),
		('PA', 'Pará'),
		('PB', 'Paraíba'),
		('PR', 'Paraná'),
		('PE', 'Pernambuco'),
		('PI', 'Piauí'),
		('RJ', 'Rio de Janeiro'),
		('RN', 'Rio Grande do Norte'),
		('RS', 'Rio Grande do Sul'),
		('RO', 'Rondônia'),
		('RR', 'Roraima'),
		('SC', 'Santa Catarina'),
		('SP', 'São Paulo'),
		('SE', 'Sergipe'),
		('TO', 'Tocantins')
	)

	name = models.CharField(max_length=140, null=True, blank=True)
	email = models.CharField(max_length=140, null=False, blank=False)
	instrument = models.CharField(max_length=400, null=False, blank=False)
	uf = models.CharField(max_length=2, null=False, blank=False, choices=UFS)
    
	def __unicode__(self):
		return self.email