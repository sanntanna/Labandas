from bands.models import Musician, Band, MusicalStyle
from django.template.defaultfilters import slugify
from equipaments.models import EquipamentType
from geoapi.models import Address
from helpers import *

RESULTS_PER_PAGE = 20

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

	results = perform_search(filters['result_kw'], 1, search_type, filters['musical_styles'], filters['instruments'])

	results['result_kw'] = filters['result_kw']

	return results

def perform_search(kw=None, page=1, search_type=SearchType.ALL, musical_styles=None, instruments=None):
	
	if search_type == SearchType.MUSICIAN:
		arguments = {}

		print instruments
		if(musical_styles != None and len(musical_styles) > 0):
			arguments['musical_styles__in'] = [s['pk'] for s in musical_styles]

		if(instruments != None and len(instruments) > 0):
			arguments['type_instruments_play__in'] = [i['pk'] for i in instruments]

		if(kw != None):
			arguments['user__first_name__icontains'] = kw			

		data = Musician.objects.filter(**arguments)[page-1:RESULTS_PER_PAGE]

		return {'musicians': data, 'count': len(data)}

	return {}


def get_filters_from_search(kw):
	n_terms = slugify(kw).split('-')

	styles = [remove_from_term(n_terms, s, s['n_name']) for s in musical_styles if s['n_name'] in n_terms]
	instruments = [remove_from_term(n_terms, e, e['n_name'], e['n_whoplay']) for e in equipaments if e['n_whoplay'] in n_terms or e['n_name'] in n_terms]

	if len(styles) > 0 or len(instruments) > 0:
		remove_unutil_words(n_terms)

	result_kw = []
	kw_arr = kw.split(' ')
	normalized_kw_arr = slugify(kw).split('-')
	i = 0

	for term in normalized_kw_arr:
		if term in n_terms:
			result_kw.append(kw_arr[i])
		i += 1

	return {
		'musical_styles': styles,
		'instruments': instruments,
		'result_kw': ' '.join(result_kw)
	}

def define_search_type(kw, filters):
	n_terms = slugify(kw).split('-')

	has_musician_kw = 'musico' in n_terms or 'musicos' in n_terms
	has_band_kw = 'banda' in n_terms  or 'bandas' in n_terms

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


