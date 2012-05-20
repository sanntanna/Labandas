from bands.forms import ExpressRegistrationForm
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
        'musicBands': request.user.get_profile().get_musician_bands(),
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