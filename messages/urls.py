from django.conf.urls import patterns

urlpatterns = patterns('messages.views',
	(r'^listar$', 'list'),
    (r'^enviar$', 'send'),
    (r'^marcar-como-lida$', 'mark_as_readed'),
    (r'^enviar-post$', 'send_post'),
)