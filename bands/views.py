from bands.forms import ExpressRegistrationForm, BandForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template.context import RequestContext
from jsonui.response import JSONResponse

def subscribe_musician(request):
    data = { "success": True }
    
    if request.method == 'POST' and request.is_ajax():  
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
    if request.method == 'POST': 
        form = BandForm(request.POST)
        if form.is_valid():
            form.save(request.user)
        
        return HttpResponseRedirect("/")
        
    t = loader.get_template('band/new.html')
    c = RequestContext(request, {
        'form': BandForm()
    })
    
    return HttpResponse(t.render(c))

