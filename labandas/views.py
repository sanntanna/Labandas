from bands.forms import ExpressRegistrationForm
from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template.context import RequestContext

def home(request):
    t = loader.get_template('home-logged.html' if request.user.is_authenticated() else 'home.html')
    c = RequestContext(request, {
        'form': ExpressRegistrationForm(),
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