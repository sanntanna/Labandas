from bands.models import Musician, Band
from django.shortcuts import get_object_or_404
from equipaments.models import EquipamentType
from http_method.BaseView import BaseView, ajax, onypostallowed
from jsonui.response import JSONResponse
from solicitations.models import Solicitation

class SolicitationMusician(BaseView):
    def _get_target_musician_id_(self, request):
        return int(request.META.get('HTTP_REFERER').split('/').pop())
    
    @ajax
    @onypostallowed
    def send(self, request):
        source_musician = request.user.get_profile()
        band = Band.objects.get(pk=request.POST['band_id'])
        target_musician = Musician.objects.get(pk=self._get_target_musician_id_(request))
        instruments_ids = request.POST.getlist('instruments')
        instruments = EquipamentType.objects.in_bulk(instruments_ids)
        
        if not Solicitation.objects.ask_to_add(source_musician, target_musician, band, instruments):
            return JSONResponse({'success': False})
        
        return JSONResponse({'success': True})
    

class RespondingSolicitation(BaseView):
    
    def _get_reply_(self, request):
        return request.path_info.split('/').pop()
    
    @ajax
    @onypostallowed
    def responding(self, request):
        reply = self._get_reply_(request)
        solicitation = get_object_or_404(Solicitation, pk=request.POST.get('id'))
        
        if reply == "aceitar":
            Solicitation.objects.accept(solicitation)
        else:
            Solicitation.objects.reject(solicitation)
            
        return JSONResponse({'success': True})