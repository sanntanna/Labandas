from django.template.defaultfilters import slugify

def normalize_musicalstyles(data):
	return [{'pk': m.pk, 'text': m.name, 'n_name': slugify(m.name)} for m in data]

def normalize_equipaments(data):
	return [{'pk': m.pk, 
			'text': m.name, 
			'n_name': slugify(m.name), 
			'n_whoplay': slugify(m.who_play)} for m in data]	

def remove_from_term(terms, key, *words):
	for w in words:
		if w in terms:
			terms.remove(w)

	return key


def remove_plural(word):
	if not word.endswith('s'):
		return word

	return word[:-1]

def remove_unutil_words(term_list):
	black_list = 'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas', 'que', 'quem', 'em', 'de', 'da', 'do', 'das', 'dos', 'para', 'por', 'e', 'ou', 'nao'

	[term_list.remove(t) for t in black_list if t in term_list]


