from bands.models import Musician
from solicitations.models import Solicitation
from jsonui.response import JSONResponse

def send_solicitation_band(request):
    source_musician = request.user.get_profile()
    band = Musician.objects.get(pk=request.POST['band_id'])
    target_musician = Musician.objects.get(pk=request.POST['musician_id'])
    
    if not Solicitation.objects.ask_musician(source_musician, target_musician, band, request.POST['instruments']):
        return JSONResponse({'success': False})
    
    return JSONResponse({'success': True})