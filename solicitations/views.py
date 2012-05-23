from bands.models import Musician, Band
from equipaments.models import EquipamentType
from http_method.BaseView import BaseView, ajax, onypostallowed
from jsonui.response import JSONResponse
from solicitations.models import Solicitation

class SolicitationMusician(BaseView):
    def __get_target_musician_id__(self, request):
        return int(request.META.get('HTTP_REFERER').split('/').pop())
    
    @ajax
    @onypostallowed
    def send(self, request):
        source_musician = request.user.get_profile()
        band = Band.objects.get(pk=request.POST['band_id'])
        target_musician = Musician.objects.get(pk=self.__get_target_musician_id__(request))
        instruments_ids = request.POST.getlist('instruments')
        instruments = EquipamentType.objects.in_bulk(instruments_ids)
        
        if not Solicitation.objects.ask_to_add(source_musician, target_musician, band, instruments):
            return JSONResponse({'success': False})
        
        return JSONResponse({'success': True})