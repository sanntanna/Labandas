#coding=ISO-8859-1
from announcements.forms import AnnouncementForm
from bands.forms import BandForm, BandMusicianForm
from bands.models import Band, MusicianBand, SetlistMusic, MusicalStyle
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect
from django.template import loader
from django.template.context import RequestContext
from httpmethod.decorators import onlypost, onlyajax
from jsonui.response import JSONResponse
from partialview.decorators import Partialhandled
from partialview.utils import HttpPartialResponseHandler
from solicitations.models import Solicitation
from medias.models import BandMedia
from equipaments.models import EquipamentType

import logging

logger = logging.getLogger('labandas')
full_template = 'bands/includes/band-wrapper.html'
partial_template = 'bands/includes/band-wrapper-partial.html'


def create_band(request):
    c = RequestContext(request, {
        'musical_styles': MusicalStyle.objects.all(),
        'equipament_types': EquipamentType.objects.all(),
    })

    t = loader.get_template('lightbox/new-band.html')

    return HttpResponse(t.render(c))

@onlypost
def create_band_post(request):
    band_name = request.POST['band_name']

    if band_name is None or band_name == "":
        return JSONResponse({'success': False})

    created_band = Band.objects.create(name=band_name)
    created_band.musical_styles=request.POST.getlist('musical_styles')
    created_band.add_musician(request.user.get_profile(), request.POST.getlist('instruments'), True)

    return JSONResponse({'success': True, 'band_page_url': created_band.page_url})

@Partialhandled(full_template, partial_template)
def band_page(request, band_id, name):  
    band = get_object_or_404(Band, pk=band_id)
    
    correct_url = band.page_url
    if correct_url != request.path_info:
        return HttpResponsePermanentRedirect(correct_url)
    
    can_edit = user_can_edit(request.user, band)
    
    template_file = 'bands/band-page.html' if can_edit else 'bands/band-page-public.html'
    template = loader.get_template(template_file)
    context_data = {
        'band': band,
        'equipament_types': EquipamentType.objects.all(),
    }

    if can_edit:
        context_data['solicitations_pending'] = Solicitation.objects.musicians_pending(band)

    context = RequestContext(request, context_data)
    
    return HttpPartialResponseHandler(template, context)

@Partialhandled(full_template, partial_template)
def band_setlist(request, name, band_id):
    band = get_object_or_404(Band, pk=band_id)

    correct_url = band.setlist_url
    if correct_url != request.path_info:
        return HttpResponsePermanentRedirect(correct_url)

    t = loader.get_template("bands/band-setlist.html")
    c = RequestContext(request, {
        'band': band,
        'can_edit': user_can_edit(request.user, band)
    })
    
    return HttpPartialResponseHandler(t, c)

@Partialhandled(full_template, partial_template)
def band_photos(request, name, band_id):
    band = get_object_or_404(Band, pk=band_id)

    correct_url = band.photos_url
    if correct_url != request.path_info:
        return HttpResponsePermanentRedirect(correct_url)

    template = loader.get_template("bands/band-photos.html")
    context = RequestContext(request, {
        'band': band,
        'can_edit': user_can_edit(request.user, band),
        'photos': band.media.photos
    })
    
    return HttpPartialResponseHandler(template, context)

@Partialhandled(full_template, partial_template)
def band_videos(request, name, band_id):
    band = get_object_or_404(Band, pk=band_id)

    correct_url = band.videos_url
    if correct_url != request.path_info:
        return HttpResponsePermanentRedirect(correct_url)

    template = loader.get_template("bands/band-videos.html")
    context = RequestContext(request, {
        'band': band,
        'can_edit': user_can_edit(request.user, band),
        'videos': band.media.videos
    })
    
    return HttpPartialResponseHandler(template, context)

@Partialhandled(full_template, partial_template)
def band_history_ads(request, name, band_id):
    band = get_object_or_404(Band, pk=band_id)

    template = loader.get_template("bands/history-ads.html")
    context = RequestContext(request, {
        'band': band,
        'can_edit': user_can_edit(request.user, band)
    })
    
    return HttpPartialResponseHandler(template, context)

@onlypost
@onlyajax
def update_field(request, field):

    updated_field = request.POST.getlist(field) if not request.POST.get('single') else request.POST.get(field)
    band = Band.objects.get(pk=request.GET.get('id'))

    setattr(band, field, updated_field)

    band.save()
    return JSONResponse({ "success": True })

@onlypost
@onlyajax
def update_obj_field(request, obj, attr):

    updated_attr = request.POST.get(attr)

    band = Band.objects.get(pk=request.GET.get('id'))

    band_obj = getattr(band, obj)

    setattr(band_obj, attr, updated_attr)

    band.save()
    band_obj.save()
    
    return JSONResponse({ "success": True })

@onlypost
def update_cover_photo(request, band_id):
    band = Band.objects.get(pk=band_id)
    band.media.cover = request.FILES.get('img')

    return redirect(band.page_url)


@onlypost
@onlyajax
def update_setlist(request):
    band = Band.objects.get(pk=request.POST.get('id'))

    if not 'all-setlist' in request.POST:
        music = band.add_music_to_setlist(request.POST.get('music'))
        return JSONResponse({ "success": True, "music_title":  music.title, "music_id": music.id})

    musics = request.POST.get('all-setlist').splitlines(True)
    band.add_music_to_setlist(musics)

    return JSONResponse({ "success": True })

@onlypost
@onlyajax
def remove_music_from_setlist(request):
    SetlistMusic.objects.get(id=request.POST.get('id')).delete()
    return JSONResponse({ "success": True })

@onlyajax
@onlypost
def remove_band_from_band(request):
    #TODO: adicionar validação para nao remover todos os admins, sempre deve ficar um
    success = bandBand.objects.get(pk=request.POST.get('id')).deactivate()
    return JSONResponse({'success': success})

def user_can_edit(user, band):
    return hasattr(user, 'get_profile') and user.get_profile().is_in_band(band)

@onlypost
def add_photo(request):
    band = Band.objects.get(pk=request.POST.get('id'))
    band.media.add_photo(request.FILES['img'])

    return redirect(band.photos_url)

@onlyajax
def delete_photo(request):
    id_photo = request.GET['id']
    band = Band.objects.get(pk=request.GET['band_id'])
    band.media.remove_photo(id_photo)

    return JSONResponse({'success': True}) 


@onlypost
@onlyajax
def add_video(request):
    band = Band.objects.get(pk=request.POST.get('id'))
    band.media.add_video(request.POST['video'])

    return JSONResponse({'success': True}) 

@onlyajax
def delete_video(request):
    id_photo = request.GET['id']
    band = Band.objects.get(pk=request.GET['band_id'])
    band.media.remove_photo(id_photo)

    return JSONResponse({'success': True}) 