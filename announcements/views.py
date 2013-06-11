#coding=ISO-8859-1
from announcements.forms import AnnouncementForm
from announcements.models import Announcement
from bands.models import Band
from equipaments.models import EquipamentType
from httpmethod.decorators import onlyajax, onlypost
from jsonui.response import JSONResponse


@onlyajax
@onlypost
def new_announcement(request):
	form = AnnouncementForm(request.POST)

	if not form.is_valid():
		return JSONResponse({'success': False, 'errors': form.errors})

	announcement = form.save(commit=False)
	announcement.owner_band = Band(id=request.POST.get('band_id'))
	announcement.save()

	print EquipamentType(id=5)
	announcement.instruments = [EquipamentType(id=i) for i in request.POST.getlist('instruments')]

	return JSONResponse({ "success": True })


@onlyajax
@onlypost
def candidate_to_announcement(request):
	announcement = Announcement.objects.get(id=request.POST.get('id'))
	success = announcement.add_candidate(request.user.get_profile())

	return JSONResponse({ "success": success})