from bands.forms import ExpressRegistrationForm
from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template.context import RequestContext
from jsonui.response import JSONResponse
from solicitations.models import Solicitation

def home(request):
    if request.user.is_authenticated():
        return homeLogged(request)
    
    t = loader.get_template('home.html')
    c = RequestContext(request, {
        'form': ExpressRegistrationForm(),
    })
    c.update(csrf(request))
    
    return HttpResponse(t.render(c))

def homeLogged(request):
    t = loader.get_template('home-logged.html')
    musician = request.user.get_profile()
    c = RequestContext(request, {
        'music_bands': musician.get_musician_bands(),
        'band_solicitations': Solicitation.objects.band_pending(musician)
    })
    
    return HttpResponse(t.render(c))

def login(request):
    user = auth.authenticate(username=request.POST['user'], password=request.POST['password'])
    
    if user == None:
        return JSONResponse({'success': False, 'errors': {'login':["Usuario e/ou senha invalidos"]}})
    
    auth.login(request, user)
    return JSONResponse( { 'success': True, 'user': user })

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")