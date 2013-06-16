from django.http import HttpResponse
from django.template import loader
from django.template.context import RequestContext
import workers

def do_search(request):
    t = loader.get_template('search-result.html')
    c = RequestContext(request, {
        'results': workers.search(request.GET['kw'],1)
    })
    
    return HttpResponse(t.render(c))