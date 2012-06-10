#coding=ISO-8859-1
from django.utils.encoding import smart_str
from django.utils.http import urlquote
from pyquery import PyQuery as pq

class AddressFinder(object):
    #CORREIOS_URL = "http://m.correios.com.br/movel/buscaCepConfirma.do?metodo=buscarCep&cepEntrada=%s"
    CORREIOS_URL = "http://www.buscacep.correios.com.br/servicos/dnec/consultaLogradouroAction.do"
    MAPS_URL = "http://maps.googleapis.com/maps/api/geocode/xml?address=%s&sensor=false"
    
    def find(self, cep):
        result = self.get_address(cep)
        
        if result.status == Status.NOT_FOUND: 
            return result
        
        self.fill_lat_long(result.address)
        
        return result
    
    def get_address(self, cep):
        page = pq(url=self.CORREIOS_URL, method="POST", data={'relaxation': cep, 'Metodo':'listaLogradouro', 'TipoConsulta': 'relaxation'})
        content = page.find(".ctrlcontent > div table:first tr")
        error = page.find("title:contains('Erro')").html()
        
        result = SearchAddrResult()
        
        if not error is None:
            result.message = error
            result.status = Status.NOT_FOUND
            return result
        
        address = Address()
        address.street = self.__addr_field(0, content)
        address.district = self.__addr_field(1, content)
        address.city = self.__addr_field(2, content)
        address.state =  self.__addr_field(3, content)
        
        result.address = address
        result.status = Status.FOUND
        return result
    
    def __addr_field(self, index, parent):
        content = parent.find('td')[index].text
        return None if content is None else content.strip()
    
    def fill_lat_long(self, address):
        addr_xml = pq(self.MAPS_URL % urlquote(str(address)))
        status = addr_xml.find("geocoderesponse status").html()
        
        if status == "ZERO_RESULTS":
            address.latitude= 0.0
            address.longitude = 0.0
            address.status = Status.NO_GEOPOSITION
            
        lat_long_node =  addr_xml.find('geometry location')
    
        address.latitude = float(lat_long_node.find('lat').html())
        address.longitude = float(lat_long_node.find('lng').html())

class Status():
    FOUND = 1
    NOT_FOUND = 2
    NO_GEOPOSITION = 3

class Address(object):
    cep = None
    street = None
    district = None
    city = None
    state = None
    country = "Brasil"
    latitude = 0.0
    longitude = 0.0
    
    def __with_comma(self, key):
        return "" if key is None else "%s," % key
    
    def __str__(self):
        complete_address = "%s %s %s %s" % (self.__with_comma(self.street), self.__with_comma(self.city), self.__with_comma(self.state), self.__with_comma(self.country))
        return smart_str(complete_address).rstrip(",")
    
class SearchAddrResult(object):
    address = None
    status = None
    message = None