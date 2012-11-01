#coding=ISO-8859-1
from django.db import models

class Record(models.Model):

	UFS = (
		(u'AC', u'Acre'),
		(u'AL', u'Alagoas'),
		(u'AP', u'Amapá'),
		(u'AM', u'Amazonas'),
		(u'BA', u'Bahia '),
		(u'CE', u'Ceará'),
		(u'DF', u'Distrito Federal'),
		(u'ES', u'Espírito Santo'),
		(u'GO', u'Goiás'),
		(u'MA', u'Maranhão'),
		(u'MT', u'Mato Grosso'),
		(u'MS', u'Mato Grosso do Sul'),
		(u'MG', u'Minas Gerais'),
		(u'PA', u'Pará'),
		(u'PB', u'Paraíba'),
		(u'PR', u'Paraná'),
		(u'PE', u'Pernambuco'),
		(u'PI', u'Piauí'),
		(u'RJ', u'Rio de Janeiro'),
		(u'RN', u'Rio Grande do Norte'),
		(u'RS', u'Rio Grande do Sul'),
		(u'RO', u'Rondônia'),
		(u'RR', u'Roraima'),
		(u'SC', u'Santa Catarina'),
		(u'SP', u'São Paulo'),
		(u'SE', u'Sergipe'),
		(u'TO', u'Tocantins')
	)

	name = models.CharField(max_length=140, null=True, blank=True)
	email = models.CharField(max_length=140, null=False, blank=False)
	instrument = models.CharField(max_length=400, null=False, blank=False)
	uf = models.CharField(max_length=2, null=False, blank=False, choices=UFS)
    
	def __unicode__(self):
		return self.email