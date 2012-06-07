from bands.forms import ExpressRegistrationForm, UserInfoForm
from bands.models import Musician
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.template import loader
from django.template.context import RequestContext
from httpmethod.decorators import onlyajax, onlypost
from jsonui.response import JSONResponse

@onlypost
@onlyajax
def subscribe_musician(request):
    form = ExpressRegistrationForm(request.POST)
    
    if not form.is_valid():
        return JSONResponse({'success': False, 'errors': form.errors})
    
    form.save()
    user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
    login(request, user)
    return JSONResponse({'success': True, 'user': user})

@onlyajax
def update_cep(request):
    if request.GET["cep"] == "":
        return JSONResponse({ "success": False })
    
    musician = request.user.get_profile() 
    musician.set_cep(request.GET["cep"])
    musician.save()
    return JSONResponse({ "success": True })

def edit_musician(request):
    t = loader.get_template('bands/edit-musician.html')
    c = RequestContext(request, {'form': UserInfoForm(instance=request.user)})
    
    return HttpResponse(t.render(c))

@onlypost
@onlyajax
def edit_musician_post(request):
    form = UserInfoForm(data=request.POST, instance=request.user)
    if not form.is_valid():
        return JSONResponse({'success':False, 'errors': form.errors})
    
    form.save()
    return JSONResponse({'success': True})

def profile(request, user_id, name):
    owner = get_object_or_404(Musician, pk=user_id)
    
    correct_url = owner.encode_profile()
    if correct_url != request.path_info:
        return HttpResponsePermanentRedirect(correct_url)
    
    t = loader.get_template('bands/musician-profile.html')
    
    c = RequestContext(request, {
        'owner': owner,
    })
    
    return HttpResponse(t.render(c))

@onlyajax    
def search_musician(request):
    search = request.GET.get('q')
    musicians = Musician.objects.filter(user__first_name__icontains=search).values('pk', 'user__first_name')
    return JSONResponse({'success': True, 'musicians': musicians}) 

@onlyajax
def get_bands(request):
    bands = [{'id': b.id, 'name': b.name} for b in request.user.get_profile().bands_list]
    return JSONResponse({'success': True, 'bands':bands})