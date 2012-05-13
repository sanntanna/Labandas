from bands.forms import ExpressRegistrationForm, BandForm
from django.template import loader
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.template.context import RequestContext
from jsonui.response import JSONResponse


def subscribe(request):
    data = { "success": True }
    
    if request.method == 'POST': 
        form = ExpressRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            login(request, user)
        else:
            data["errors"] = form.errors
            data["success"] = False

    return JSONResponse(data)

def add_band(request):
    t = loader.get_template('band/new.html')
    c = RequestContext(request, {
        'form': BandForm()
    })
    
    return HttpResponse(t.render(c))