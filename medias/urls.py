from django.conf.urls import patterns

urlpatterns = patterns('medias.views',
	(r'^atualizar-legenda$', 'update_legend'),
)