#coding=UTF-8
import datetime

from bands.forms import ExpressRegistrationForm
from bands.models import Musician
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect
from django.template import loader
from django.template.context import RequestContext
from httpmethod.decorators import onlyajax, onlypost
from jsonui.response import JSONResponse
from partialview.decorators import Partialhandled
from partialview.utils import HttpPartialResponseHandler
from medias.models import MusicianMedia
from solicitations.models import Solicitation
from bands.models import MusicalStyle
from equipaments.models import EquipamentType

full_template = 'bands/includes/musician-wrapper.html'
partial_template = 'bands/includes/musician-wrapper-partial.html'

@Partialhandled(full_template, partial_template)
def profile(request):
    t = loader.get_template('bands/musician-profile.html')
    musician = request.user.get_profile()
    has_personal_data = musician.type_instruments_play.all().count() > 0 \
                        and musician.musical_styles.all().count() > 0 \
                        and not musician.address.city is None

    c = RequestContext(request, {
        'musical_styles': MusicalStyle.objects.all(),
        'equipament_types': EquipamentType.objects.all(),
        'has_personal_data': has_personal_data,
        'musician':musician
    })
    
    return HttpPartialResponseHandler(t, c)

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

@Partialhandled(full_template, partial_template)
def public_profile(request, user_id, name):
    musician = get_object_or_404(Musician, pk=user_id)
    
    correct_url = musician.profile_url
    if correct_url != request.path_info:
        return HttpResponsePermanentRedirect(correct_url)
    
    template = loader.get_template('bands/musician-public-profile.html')
    context = RequestContext(request, {
        'musician': musician,
        'current_year': datetime.datetime.now().year
    })
    
    return HttpPartialResponseHandler(template, context)

@Partialhandled(full_template, partial_template)
def musician_photos(request, name, user_id):
    musician = get_object_or_404(Musician, pk=user_id)

    template = loader.get_template("bands/musician-photos.html")
    context = RequestContext(request, {
        'musician': musician,
    })
    
    return HttpPartialResponseHandler(template, context)

@Partialhandled(full_template, partial_template)
def musician_videos(request, name, user_id):
    musician = get_object_or_404(Musician, pk=user_id)

    template = loader.get_template("bands/musician-videos.html")
    context = RequestContext(request, {
        'musician': musician,
    })
    
    return HttpPartialResponseHandler(template, context)

@Partialhandled(full_template, partial_template)
def musician_bands(request, name, user_id):
    musician = get_object_or_404(Musician, pk=user_id)

    template = loader.get_template("bands/musician-bands.html")
    context = RequestContext(request, {
        'musician': musician,
    })
    
    return HttpPartialResponseHandler(template, context)

@onlyajax
def find_musician(request):
    search = request.GET.get('kw')
    musicians = Musician.objects.filter(user__first_name__icontains=search, id__gt=1)

    response = [{'name': m.name(), 'avatar': m.media.avatar, 'id': m.id} for m in musicians]
    return JSONResponse({'success': True, 'musicians': response}) 


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