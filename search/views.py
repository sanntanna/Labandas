from django.http import HttpResponse
from django.template import loader
from django.template.context import RequestContext
import workers

def do_search(request):
    t = loader.get_template('search-result.html')

    current_page = 1 if not 'pg' in request.GET else int(request.GET['pg'])
    c = RequestContext(request, {
        'results': workers.search(request.GET['kw'], current_page)
    })
    
    return HttpResponse(t.render(c))