from django.contrib.gis.geos import Point
from django.utils.http import urlquote
from models import Address

from pyquery import PyQuery as pq

class AddressFinder(object):
    CORREIOS_URL = "http://m.correios.com.br/movel/buscaCepConfirma.do?metodo=buscarCep&cepEntrada=%s"
    MAPS_URL = "http://maps.googleapis.com/maps/api/geocode/xml?address=%s&sensor=false"
    
    def find(self, cep):
        result = self.__get_address(cep)
        
        if result.status == SearchAddrStatus.NOT_FOUND: 
            return result
        
        result.point = self.__get_point(result.address)

        if result.point is None:
            result.status = SearchAddrStatus.NO_GEOPOSITION

        return result
    
    def __get_address(self, cep):
        page = pq(url=self.CORREIOS_URL % cep)
        fields = page.find(".resposta")
        err = page.find(".erro").text()
        
        result = SearchAddrResult()

        if not err is None:
            result.message = err
            result.status = SearchAddrStatus.NOT_FOUND
            return result

        city, state = self.__get_field(fields, "Localidade / UF").split('/')

        address = Address()
        address.street = self.__get_field(fields, "Logradouro")
        address.district = self.__get_field(fields, "Bairro")
        address.city = city.strip('\n').strip()
        address.state =  state.strip('\n').strip()
        address.cep = cep
        
        result.address = address
        result.status = SearchAddrStatus.FOUND
        
        return result
    
    def __get_point(self, address):
        addr_xml = pq(self.MAPS_URL % urlquote(str(address)))
        status = addr_xml.find("geocoderesponse status").html()
        
        if status == "ZERO_RESULTS":
            return None
            
        lat_long_node =  addr_xml.find('geometry location')
    
        return  Point(float(lat_long_node.find('lat').html()), float(lat_long_node.find('lng').html()))

    def __get_field(self, fields, name):
        selected_field = fields.filter(lambda i: pq(this).text().rstrip(":") == name)

        if not len(selected_field):
            return None
        return selected_field.next(".respostadestaque").text().strip()


class SearchAddrStatus():
    FOUND = 1
    NOT_FOUND = 2
    NO_GEOPOSITION = 3
    
class SearchAddrResult(object):
    address = None
    status = None
    message = None
    location_point = None

finder = AddressFinder()