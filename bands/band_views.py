#coding=ISO-8859-1
from announcements.forms import AnnouncementForm
from bands.forms import BandForm, BandMusicianForm
from bands.models import Band, MusicianBand
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.template import loader
from django.template.context import RequestContext
from httpmethod.decorators import onlypost, onlyajax
from jsonui.response import JSONResponse
from solicitations.models import Solicitation
import logging


logger = logging.getLogger('labandas')

@onlypost
def create_band(request):
    band_name = request.POST['band_name']

    if band_name is None or band_name == "":
        return JSONResponse({'success': False})

    created_band = Band.objects.create(name=band_name)
    created_band.add_musician(request.user.get_profile(), None, True)

    return JSONResponse({'success': True, 'band_page_url': created_band.page_url})
    
def band_page(request, band_id, name):  
    band = get_object_or_404(Band, pk=band_id)
    
    correct_url = band.page_url
    if correct_url != request.path_info:
        return HttpResponsePermanentRedirect(correct_url)
    
    t = loader.get_template('bands/band-page.html')
    c = RequestContext(request, {
        'band': band,
    })
    
    return HttpResponse(t.render(c))

@onlyajax
@onlypost
def remove_musician_from_band(request):
    #TODO: adicionar validação para nao remover todos os admins, sempre deve ficar um
    success = MusicianBand.objects.get(pk=request.POST.get('id')).deactivate()
    return JSONResponse({'success': success})

