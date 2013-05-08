from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.template.context import RequestContext
from httpmethod.decorators import onlyajax, onlypost
from jsonui.response import JSONResponse
from models import Message


def send(request):
	recipient = get_object_or_404(User, pk=request.GET['id'])
	c = RequestContext(request, {
		'recipient': recipient,
	})

	t = loader.get_template('lightbox/send-message.html')
	return HttpResponse(t.render(c))

@onlypost
@onlyajax
def send_post(request):
	recipient = User.objects.get(id=request.POST['recipient_id'])
	Message.objects.send_message(request.user, recipient, None, request.POST['message'])

	return JSONResponse({'success':True})

@onlyajax
def mark_as_readed(request):
	Message.objects.mark_as_read(request.GET.getlist('ids'))

	return JSONResponse({'success':True})

@onlyajax
def list(request):
	objects = request.user.messages_received.filter(active=True).all()

	messages = [{	'id': o.id, 
					'is_read': o.read_date != None,
					'from_id': o.from_user.id,
					'from': o.from_user.get_full_name(), 
					'from_avatar': o.from_user.get_profile().media.avatar_small, 
					'message': o.text,
					'subject': o.subject } for o in objects]

	return JSONResponse({'success':True, 'messages': messages})	
