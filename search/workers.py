from bands.models import Musician, Band, MusicalStyle
from django.template.defaultfilters import slugify
from equipaments.models import EquipamentType
from geoapi.models import Address
from helpers import *

class SearchType(object):
	ALL = 0
	MUSICIAN = 1
	BAND = 2

equipaments = normalize_equipaments(EquipamentType.objects.all())
musical_styles = normalize_musicalstyles(MusicalStyle.objects.all())
ufs = Address.objects.values('district')


def search(kw):
	filters = get_filters_from_search(kw)

	search_type = define_search_type(kw, filters)

	print filters['musical_styles']
	print filters['instruments']
	print filters['result_kw']

	print search_type

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

def define_search_type(kw, filters):
	n_terms = slugify(kw).split('-')

	has_musician_kw = 'musico' in n_terms
	has_band_kw = 'banda' in n_terms 

	if  has_musician_kw and not has_band_kw:
		return SearchType.MUSICIAN

	if has_band_kw and not has_musician_kw:
		return SearchType.BAND

	if has_musician_kw and has_band_kw:
		return SearchType.MUSICIAN if n_terms.index('musico') < n_terms.index('banda') else SearchType.BAND

	who_plays = [w for w in equipaments if w['n_whoplay'] in n_terms]

	if len(who_plays) > 0:
		return SearchType.MUSICIAN

	return SearchType.ALL		


