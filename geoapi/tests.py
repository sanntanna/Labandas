#coding=ISO-8859-1
from django.test import TestCase
from geoapi.models import Status, AddressFinder, Address


class GeoLocalizationTest(TestCase):
    
    def deve_recuperar_informacoes_endereco(self):
        finder = AddressFinder()
        result = finder.get_address("03264-040")
        address = result.address
        
        self.assertEquals(Status.FOUND, result.status)
        
        self.assertEquals(u"Rua Roque Barbosa Lima", address.street)
        self.assertEquals(u"Vila Paulo Silas", address.district)
        self.assertEquals(u"São Paulo", address.city)
        self.assertEquals(u"SP", address.state)
    
    def deve_recuperar_latitude_longitude(self):
        address = Address() 
        address.state = u"SP"
        address.city = u"São Paulo"
        address.district = u"Vila Paulo Silas"
        address.street = u"Rua Roque Barbosa Lima"
        
        finder = AddressFinder()
        finder.fill_lat_long(address)
        
        self.assertEquals(-23.5899937, address.latitude)
        self.assertEquals(-46.5450177, address.longitude)
    
    def test_recupearar_informacoes_consolidadas(self):
        finder = AddressFinder()
        result = finder.find("03264-040")
        address = result.address
        
        self.assertEquals(Status.FOUND, result.status)
        
        self.assertEquals(u"Rua Roque Barbosa Lima", address.street)
        self.assertEquals(u"Vila Paulo Silas", address.district)
        self.assertEquals(u"São Paulo", address.city)
        self.assertEquals(u"SP", address.state)
        self.assertEquals(-23.5899937, address.latitude)
        self.assertEquals(-46.5450177, address.longitude)
    
    def test_deve_tratar_endereco_nao_encontrado(self):
        finder = AddressFinder()
        result = finder.find("69903-570") #cep do acre
        self.assertEquals(Status.NOT_FOUND, result.status)
    
    def teste_deve_tratar_endereco_incompleto(self):
        finder = AddressFinder()
        
        result = finder.find("36240-000") #cep MG
        self.assertEquals(Status.FOUND, result.status)
        address = result.address
        
        self.assertIsNone(address.street)
        self.assertIsNone(address.district)
        
        self.assertEquals(-21.4579215, address.latitude)
        self.assertEquals(-43.5528051, address.longitude)
        
    def test_deve_tratar_endereco_sem_lat_long(self):
        finder = AddressFinder()
        result = finder.find("69900-110") #TODO: encontrar um ceo que o google não ache