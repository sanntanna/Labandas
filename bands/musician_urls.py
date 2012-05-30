from django.conf.urls import patterns

urlpatterns = patterns('bands.musician_views',
    (r'^cadastrar$', 'subscribe_musician'),
    (r'^atualizar-endereco$', 'update_cep'),
    (r'^editar$', 'edit_musician'),
    (r'^editar/post$', 'edit_musician_post'),
    (r'^(?P<name>[a-z-]+)/(?P<user_id>\d+)$', 'profile'),
    (r'^buscar$', 'search_musician'),
    (r'^bandas$', 'get_bands'),
)