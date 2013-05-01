from django.conf.urls import patterns

urlpatterns = patterns('messages.views',
	(r'^listar$', 'list'),
    (r'^enviar$', 'send'),
    (r'^enviar-post$', 'send_post'),
)