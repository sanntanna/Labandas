#coding=ISO-8859-1
from django.utils.encoding import smart_str
from django.utils.http import urlquote
from pyquery import PyQuery as pq

class Status():
    FOUND = 1
    NOT_FOUND = 2
    NOT_GEOPOSITION = 3

class Address(object):
    cep = ""
    street = ""
    district = ""
    city = ""
    state = ""
    country = "Brasil"
    latitude = 0.0
    longitude = 0.0
    
    def _with_comma_(self, key):
        return key + u"," if key != "" else ""
    
    def __str__(self):
        complete_address = "%s %s %s %s" % (self._with_comma_(self.street), self._with_comma_(self.city), self._with_comma_(self.state), self._with_comma_(self.country))
        return smart_str(complete_address).rstrip(",")
    
class SearchAddrResult(object):
    address = None
    status = None

def get_localization(cep):
    result = get_address(cep)
    if result.status == Status.NOT_FOUND: 
        return result
    
    lat_lng = get_lat_long(result.address)
    result.address.latitude = lat_lng['lat']
    result.address.longitude = lat_lng['lng']
    
    return result
    

def get_address(cep):
    CORREIOS_URL = "http://m.correios.com.br/movel/buscaCepConfirma.do?metodo=buscarCep&cepEntrada=%s"
    def _run_(cep):
        page = pq(CORREIOS_URL % cep)
        content = page.find(".caixacampobranco:first")
        
        error = page.find(".erro:first").html()
        
        result = SearchAddrResult()
        
        if not error is None:
            result.status = Status.NOT_FOUND
            return result
        
        address = Address()
        address.status = Status.FOUND
        address.street = _addr_field_("Logradouro", content)
        address.district = _addr_field_("Bairro", content)
        
        city, state = _addr_field_("Localidade / UF", content).split("/")
        address.city = city.strip()
        address.state =  state.strip() 
    
        
        result.address = address
        result.status = Status.FOUND
        return result
    
    def _addr_field_(name, parent):
        content = parent.find('.resposta:contains("%s") ~ .respostadestaque' % name).html()
        return "" if content is None else content.strip()
    
    return _run_(cep)

def get_lat_long(address):
    MAPS_URL = "http://maps.googleapis.com/maps/api/geocode/xml?address=%s&sensor=false"
    addr_xml = pq(MAPS_URL % urlquote(str(address)))
    status = addr_xml.find("geocoderesponse status").html()
    
    if status == "ZERO_RESULTS":
        return {'lat':0.0, 'lng': 0.0}
    
    lat_long_node =  addr_xml.find('geometry location')

    return {
        'lat': float(lat_long_node.find('lat').html()),
        'lng': float(lat_long_node.find('lng').html())
    }