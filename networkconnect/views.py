#coding=ISO-8859-1
from networkconnect.models import UserNetwork
from jsonui.response import JSONResponse


def connect(request):
	network_token = request.POST.get('token')
	network_name = request.POST.get('name')

    
    return JSONResponse({'success': True})
