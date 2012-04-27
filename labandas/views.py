from bands.forms import ExpressRegistrationForm
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.template import loader
from django.template.context import RequestContext

def home(request):
    t = loader.get_template('home.html')
    c = RequestContext(request, {
        'form': ExpressRegistrationForm(),
    })
    c.update(csrf(request))
    
    return HttpResponse(t.render(c))