from bands.models import Musician, Band, MusicalStyle
from django.template.defaultfilters import slugify
from equipaments.models import EquipamentType
from geoapi.models import Address


def normalize_data(data):
	return [{'pk': m.pk, 'text': m.name, 'normalized': slugify(m.name)} for m in data]

equipaments = normalize_data(EquipamentType.objects.all())
musical_styles = normalize_data(MusicalStyle.objects.all())
ufs = Address.objects.values('district')


def init():
	print equipaments

def search_kw(self=None, kw=None):
	print len(equipaments)

def search_bands(self):
	pass

def search_musicians(self):
	pass

def get_filters_from_search(self, kw):
	pass




init()