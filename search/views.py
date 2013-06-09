from django.http import HttpResponse
from django.template import loader
from django.template.context import RequestContext
import workers

def do_search(request):
    t = loader.get_template('resultado-busca.html')
    c = RequestContext(request, {
        'results': workers.search(request.GET['kw'])
    })
    
    return HttpResponse(t.render(c))