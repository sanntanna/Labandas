#coding=ISO-8859-1
from bands.forms import ExpressRegistrationForm
from bands.musician_views import profile
from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template.context import RequestContext
from jsonui.response import JSONResponse
from messages.models import Message
from solicitations.models import Solicitation

def home(request):
    if request.user.is_authenticated():
        return profile(request)
    
    t = loader.get_template('home.html')
    c = RequestContext(request, {
        'subscribe_form': ExpressRegistrationForm(),
    })
    c.update(csrf(request))
    
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

def count_notifications(request):
    totals = {
        'messages': Message.objects.total_unread_from_musician(request.user),
        'solicitations': Solicitation.objects.count_from_music_pending(request.user)
    }

    return JSONResponse({ 'success': True, 'totals': totals })
