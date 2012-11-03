#coding=ISO-8859-1
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template.context import RequestContext

from httpmethod.decorators import onlyajax, onlypost
from forms import RecordForm
from models import Record

from jsonui.response import JSONResponse

def landing_page(request):
    t = loader.get_template('landing-page.html')
    c = RequestContext(request, {
        'form': RecordForm(),
        'success': False,
    })
    c.update(csrf(request))
    
    return HttpResponse(t.render(c))

@onlypost
def landing_page_submit(request):
    form = RecordForm(request.POST)

    if not form.is_valid():
        return JSONResponse({'success': False, 'errors': form.errors})

    form.instance.save()

    t = loader.get_template('landing-page.html')
    c = RequestContext(request, {
        'success': True,
    })

    return JSONResponse({'success': True})