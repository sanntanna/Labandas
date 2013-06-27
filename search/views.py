from django.http import HttpResponse
from django.template import loader
from django.template.context import RequestContext
from bands.models import Musician
from bands.models import MusicalStyle
from equipaments.models import EquipamentType
import workers

def do_search(request):
    t = loader.get_template('search-result.html')
    musician = request.user.get_profile()

    current_page = 1 if not 'pg' in request.GET else int(request.GET['pg'])
    c = RequestContext(request, {
        'results': workers.search(request.GET['kw'], current_page),
        'musical_styles': MusicalStyle.objects.all(),
        'equipament_types': EquipamentType.objects.all(),
        'musician_instruments_play': musician.type_instruments_play.all(),
        'musician':musician
    })
    
    return HttpResponse(t.render(c))