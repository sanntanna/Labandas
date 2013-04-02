#coding=ISO-8859-1
from bands.forms import ExpressRegistrationForm
from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template.context import RequestContext
from jsonui.response import JSONResponse
from solicitations.models import Solicitation
from bands.models import MusicalStyle
from equipaments.models import EquipamentType

def home(request):
    if request.user.is_authenticated():
        return homeLogged(request)
    
    t = loader.get_template('home.html')
    c = RequestContext(request, {
        'subscribe_form': ExpressRegistrationForm(),
    })
    c.update(csrf(request))
    
    return HttpResponse(t.render(c))

def homeLogged(request):
    t = loader.get_template('home-logged.html')
    musician = request.user.get_profile()
    has_personal_data = musician.type_instruments_play.all().count() > 0 \
                        and musician.musical_styles.all().count() > 0 \
                        and not musician.address.city is None

    print musician.type_instruments_play.all().count

    c = RequestContext(request, {
        'band_solicitations': Solicitation.objects.bands_pending(musician),
        'musical_styles': MusicalStyle.objects.all(),
        'equipament_types': EquipamentType.objects.all(),
        'has_personal_data': has_personal_data,
        'musician':musician
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

def lightbox(request, lightbox_file):
    t = loader.get_template('lightbox/%s.html' % lightbox_file)
    c = RequestContext(request, request.GET)
    c.update(csrf(request))
    return HttpResponse(t.render(c))

def lightbox_login(request):
    t = loader.get_template('lightbox/login.html')
    c = RequestContext(request, {
        'subscribe_form': ExpressRegistrationForm(),
    })
    c.update(csrf(request))
    return HttpResponse(t.render(c))