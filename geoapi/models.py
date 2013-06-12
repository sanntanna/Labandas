from django.db import models
from django.utils.encoding import smart_str

class Address(models.Model):
    cep = models.CharField(max_length=9, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    
    def __init__(self, *args, **kwargs):
        super(Address, self).__init__(*args, **kwargs)
        self.country = "Brasil"

    def __str__(self):
        complete_address = "%s %s %s %s" % (self.__with_comma(self.street), self.__with_comma(self.city), \
                                                self.__with_comma(self.state), self.__with_comma(self.country))

        return smart_str(complete_address).rstrip(",")

    def __with_comma(self, key):
        return "" if key is None else "%s," % key
