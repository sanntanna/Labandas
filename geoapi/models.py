import sys
from django.db import models
from django.utils.encoding import smart_str
from django.utils.http import urlquote
from pyquery import PyQuery as pq

class Address(models.Model):
    cep = models.CharField(max_length=9, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    
    latitude = models.FloatField(null=True,blank = True)
    longitude = models.FloatField(null=True,blank = True)
    
    def __init__(self, *args, **kwargs):
        super(Address, self).__init__(*args, **kwargs)
        self.country = "Brasil"
    
    def fill_by_cep(self, cep=None):
        finder = AddressFinder()
        result = finder.find(cep or self.cep)

        if result.status == Status.NOT_FOUND:
            return
        
        self.street = result.address.street
        self.district = result.address.district
        self.city = result.address.city
        self.state = result.address.state
        
        self.latitude = result.address.latitude
        self.longitude = result.address.longitude
        
    def __with_comma(self, key):
        return "" if key is None else "%s," % key
    
    def __str__(self):
        complete_address = "%s %s %s %s" % \
                (self.__with_comma(self.street), self.__with_comma(self.city), self.__with_comma(self.state), self.__with_comma(self.country))
        return smart_str(complete_address).rstrip(",")



class AddressFinder(object):
    CORREIOS_URL = "http://m.correios.com.br/movel/buscaCepConfirma.do?metodo=buscarCep&cepEntrada=%s"
    #CORREIOS_URL = "http://www.buscacep.correios.com.br/servicos/dnec/consultaLogradouroAction.do"
    MAPS_URL = "http://maps.googleapis.com/maps/api/geocode/xml?address=%s&sensor=false"
    
    def find(self, cep):
        result = self.get_address(cep)
        
        if result.status == Status.NOT_FOUND: 
            return result
        
        self.fill_lat_long(result.address)
        
        return result
    
    def get_address(self, cep):
        page = pq(url=self.CORREIOS_URL % cep)
        fields = page.find(".respostadestaque")
        err = page.find(".erro").text()
        
        result = SearchAddrResult()

        if not err is None:
            result.message = err
            result.status = Status.NOT_FOUND
            return result
        
        city, state = fields[2].text.split('/')

        address = Address()
        address.street = fields[0].text.strip()
        address.district = fields[1].text.strip()
        address.city = city.strip('\n').strip()
        address.state =  state.strip('\n').strip()
        
        print city
        print state

        result.address = address
        result.status = Status.FOUND
        return result
    
    def fill_lat_long(self, address):
        addr_xml = pq(self.MAPS_URL % urlquote(str(address)))
        status = addr_xml.find("geocoderesponse status").html()
        
        if status == "ZERO_RESULTS":
            address.latitude= None
            address.longitude = None
            address.status = Status.NO_GEOPOSITION
            
        lat_long_node =  addr_xml.find('geometry location')
    
        address.latitude = float(lat_long_node.find('lat').html())
        address.longitude = float(lat_long_node.find('lng').html())

class Status():
    FOUND = 1
    NOT_FOUND = 2
    NO_GEOPOSITION = 3
    
class SearchAddrResult(object):
    address = None
    status = None
    message = None