#coding=ISO-8859-1
from announcements.forms import AnnouncementForm
from announcements.models import Announcement
from bands.models import Band
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

	return JSONResponse({ "success": True, "teste": 1 })