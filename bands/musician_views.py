#coding=UTF-8
import datetime

from bands.forms import ExpressRegistrationForm, UserInfoForm
from bands.models import Musician
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template import loader
from django.template.context import RequestContext
from httpmethod.decorators import onlyajax, onlypost
from jsonui.response import JSONResponse
from medias.models import MusicianMedia


@onlypost
@onlyajax
def subscribe_musician(request):
    form = ExpressRegistrationForm(request.POST)
    
    if not form.is_valid():
        return JSONResponse({'success': False, 'errors': form.errors})
    
    email = form.cleaned_data['email']

    if User.objects.filter(username=email).count():
        message = "%s ja esta cadastrado" % email
        return JSONResponse({'success': False, 'errors': {'email': [message]}})    

    form.save()
    user = authenticate(username=email, password=form.cleaned_data['password'])
    login(request, user)
    return JSONResponse({'success': True, 'user': user})

@onlypost
@onlyajax
def update_field(request, field):

    updated_field = request.POST.getlist(field) if not request.POST.get('single') else request.POST.get(field)
    musician = request.user.get_profile()

    setattr(musician, field, updated_field)

    musician.save()
    return JSONResponse({ "success": True })

@onlypost
@onlyajax
def update_obj_field(request, obj, attr):

    updated_attr = request.POST.get(attr)

    musician = request.user.get_profile()

    musician_obj = getattr(musician, obj)

    setattr(musician_obj, attr, updated_attr)

    musician.save()
    musician_obj.save()
    
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
    
    correct_url = owner.profile_url
    if correct_url != request.path_info:
        return HttpResponsePermanentRedirect(correct_url)
    
    t = loader.get_template('bands/musician-profile.html')
    
    c = RequestContext(request, {
        'owner': owner,
        'current_year': datetime.datetime.now().year
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


@onlypost
def update_avatar(request):
    musician = request.user.get_profile()
    musician.media.avatar = request.FILES.get('img')
    musician.save()

    return redirect('/')

@onlypost
def update_cover_photo(request):
    musician = request.user.get_profile()
    musician.media.cover = request.FILES.get('img')
    musician.save()

    return redirect('/')