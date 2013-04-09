#coding=ISO-8859-1
from django.contrib import auth
from models import UserNetwork
from utils import UserFinder
from jsonui.response import JSONResponse


def connect(request):
	network_token = request.POST.get('token')
	network_name = request.POST.get('name')
	network_id = request.POST.get('id')

	finder = UserFinder()
	user, is_new, extra_fields = finder.get_user(network_name, network_token, network_id)

	if is_new and 'birthday' in extra_fields:
		musician = user.get_profile()
		musician.born_year = extra_fields['birthday'].split('/')[2]
		musician.save()

	auth.login(request, user)

	return JSONResponse({'success': True})
