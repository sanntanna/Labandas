from bands.forms import ExpressRegistrationForm
from bands.models import MusicianType, Band
from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template.context import RequestContext
from jsonui.response import JSONResponse

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
    c = RequestContext(request, {
        'musicianTypes': MusicianType.objects.all(),
        'bands': Band.objects.filter(musicians=request.user),
    })
    c.update(csrf(request))
    
    return HttpResponse(t.render(c))

def login(request):
    user = auth.authenticate(username=request.POST['user'], password=request.POST['password'])
    responseData = { "success": True }
    
    if user == None:
        responseData["success"] = False
        responseData["message"] = "Usuario e/ou senha invalidos"
    else:
        auth.login(request, user)
    
    return JSONResponse(responseData)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")