from pyquery import PyQuery as pq

class GeoLocalization(object):
    
    CORREIOS_URL = "http://m.correios.com.br/movel/buscaCepConfirma.do?metodo=buscarCep&cepEntrada=%s"
    
    def get(self, cep):
        address = self._get_address_(cep)
        lat_long = self._get_lat_long_(address)
        
        address.update(lat_long)
        
        return address
    
    def _get_address_(self, cep):
        page = pq(self.CORREIOS_URL % cep)
        content = page.find(".caixacampobranco:first")
        
        city, state = self._field_("Localidade / UF", content).split("/")
        
        return {
            'street': self._field_("Logradouro", content),
            'district': self._field_("Bairro", content),
            'city': city.strip(),
            'state': state.strip(),
        }
    
    def _field_(self, name, parent):
        return parent.find('.resposta:contains("%s") ~ .respostadestaque' % name).html().strip()
    
    def _get_lat_long_(self, address):
        return {}