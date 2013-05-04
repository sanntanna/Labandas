#coding=ISO-8859-1
from bands.models import Musician, Band
from django.shortcuts import get_object_or_404
from equipaments.models import EquipamentType
from httpmethod.decorators import onlyajax, onlypost
from jsonui.response import JSONResponse
from solicitations.models import Solicitation

@onlyajax
@onlypost
def send_solicitation(request):
    source_musician = request.user.get_profile()
    band = Band.objects.get(pk=request.POST.get('band'))
    target_musician = Musician.objects.get(pk=request.POST.get('target'))
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


@onlyajax
def list_solicitations(request):
    solicitations = Solicitation.objects.all_from_music_pending(request.user)

    res = [{    'id': s.pk, 
                'from': s.from_musician, 
                'from_id': s.from_musician.id, 
                'from_url': s.from_musician.profile_url, 
                'from_avatar': s.from_musician.media.avatar_small,
                'band': s.band.name,
                'instruments': [i.name for i in s.instruments.all()],} for s in solicitations]

    return JSONResponse({'solicitations': res})