from bands.forms import ExpressRegistrationForm
from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template.context import RequestContext
from bands.models import MusicianType

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
    })
    c.update(csrf(request))
    
    return HttpResponse(t.render(c))

def login(request):
    user = auth.authenticate(username=request.POST['user'], password=request.POST['password'])
    auth.login(request, user)
    return  HttpResponse("{s:1}")

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")