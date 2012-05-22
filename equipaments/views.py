from equipaments.models import EquipamentType
from jsonui.response import JSONResponse

def get_instruments(request):
    instruments = EquipamentType.objects.all()
    return JSONResponse({'success': True, 'instruments':instruments})