from django.conf.urls import patterns

urlpatterns = patterns('solicitations.views',
	(r'^listar$', 'list_solicitations'),
    (r'^enviar-para-musico$', 'send_solicitation'),
    (r'^aceitar$', 'respond_solicitation'),
    (r'^recusar$', 'respond_solicitation'),
    (r'^cancelar$', 'cancel_solicitation'),
)