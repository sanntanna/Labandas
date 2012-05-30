#coding=ISO-8859-1
from bands.models import Musician, Band
from django.shortcuts import get_object_or_404
from equipaments.models import EquipamentType
from http_method.decorators import onlyajax, onlypost
from jsonui.response import JSONResponse
from solicitations.models import Solicitation

@onlyajax
@onlypost
def send_solicitation(request):
    source_musician = request.user.get_profile()
    band = Band.objects.get(pk=request.POST.get('band_id'))
    target_musician = Musician.objects.get(pk=request.POST.get('target_id'))
    instruments_ids = request.POST.getlist('instruments')
    instruments = EquipamentType.objects.in_bulk(instruments_ids)
    
    if not Solicitation.objects.ask_to_add(source_musician, target_musician, band, instruments):
        return JSONResponse({'success': False})
    
    return JSONResponse({'success': True})
    

@onlyajax
@onlypost
def respond_solicitation(request):
    def _get_reply_(request):
        return request.path_info.split('/').pop()

    reply = _get_reply_(request)
    solicitation = get_object_or_404(Solicitation, pk=request.POST.get('id'))
    success = False
    if reply == "aceitar":
        success = solicitation.accept(request.user.get_profile())
    else:
        success = solicitation.reject(request.user.get_profile())
        
    return JSONResponse({'success': success})

@onlyajax
@onlypost
def cancel_solicitation(request):
    solicitation = Solicitation.objects.get(pk=request.POST.get("id"))
    return JSONResponse({'success': solicitation.cancel(request.user)})