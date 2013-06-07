from bands.models import Musician, Band, MusicalStyle
from django.template.defaultfilters import slugify
from equipaments.models import EquipamentType
from geoapi.models import Address
from helpers import *

equipaments = normalize_equipaments(EquipamentType.objects.all())
musical_styles = normalize_musicalstyles(MusicalStyle.objects.all())
ufs = Address.objects.values('district')


def search_kw(kw):
	filters = get_filters_from_search(kw)

	print filters['musical_styles']
	print filters['instruments']
	print filters['result_kw']

def search_bands(self):
	pass

def search_musicians(self):
	pass

def get_filters_from_search(kw):
	n_terms = slugify(kw).split('-')

	styles = [remove_from_term(n_terms, s, s['n_name']) for s in musical_styles if s['n_name'] in n_terms]
	instruments = [remove_from_term(n_terms, e, e['n_name'], e['n_whoplay']) for e in equipaments if e['n_whoplay'] in n_terms or e['n_name'] in n_terms]

	if len(styles) > 0 or len(instruments) > 0:
		remove_unutil_words(n_terms)

	return {
		'musical_styles': styles,
		'instruments': instruments,
		'result_kw': '-'.join(n_terms)
	}