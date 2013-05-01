from httpmethod.decorators import onlyajax, onlypost
from jsonui.response import JSONResponse
from models import Message

@onlypost
@onlyajax
def send(request):
	recipient = User(id=request.POST['recipient_id'])
	Message.objects.send_message(request.user, recipient, request.post['subject'], request.post['message'])

	return JSONResponse({success:True})

@onlyajax
def list(request):
	objects = request.user.messages_received.filter(active=True).all()

	messages = [{	'id': o.id, 
					'from': o.from_user, 
					'from_avatar': o.from_user.get_profile().avatar_small, 
					'message': o.message,
					'subject': o.subject } for o in objects]

	return JSONResponse({'success':True, 'messages': messages})	
