from bands.models import Musician
from http_method.BaseView import BaseView, ajax, onypostallowed
from jsonui.response import JSONResponse
from solicitations.models import Solicitation

class SolicitationMusician(BaseView):
    def __get_target_musician_id__(self, request):
        return request.META.get('HTTP_REFERER')
    
    @ajax
    @onypostallowed
    def send(self, request):
        source_musician = request.user.get_profile()
        band = Musician.objects.get(pk=request.POST['band_id'])
        target_musician = Musician.objects.get(pk=self.__get_target_musician_id__(request))
        
        if not Solicitation.objects.ask_musician(source_musician, target_musician, band, request.POST['instruments']):
            return JSONResponse({'success': False})
        
        return JSONResponse({'success': True})