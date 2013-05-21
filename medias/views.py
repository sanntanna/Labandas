#coding=ISO-8859-1
from models import Media
from django.shortcuts import get_object_or_404
from httpmethod.decorators import onlyajax, onlypost
from jsonui.response import JSONResponse

@onlypost
@onlyajax
def update_legend(request):
	media = Media.objects.get(id=request.POST['id'])
	media.legend = request.POST['legend']
	media.save()
	
	return JSONResponse({'success':True})
