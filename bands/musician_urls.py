from django.conf.urls import patterns

urlpatterns = patterns('bands.musician_views',
    (r'^cadastrar$', 'subscribe_musician'),
    (r'^editar$', 'edit_musician'),
    (r'^editar/post$', 'edit_musician_post'),
    (r'^atualizar/(?P<field>[a-z_]+)$', 'update_field'),
    (r'^atualizar/(?P<obj>[a-z_]+)/(?P<attr>[a-z_]+)$', 'update_obj_field'),
    (r'^(?P<name>[a-z-]+)/(?P<user_id>\d+)$', 'profile'),
    (r'^buscar$', 'search_musician'),
    (r'^bandas$', 'get_bands'),
    (r'^atualizar-imagem-perfil$', 'update_avatar'),
    (r'^atualizar-imagem-capa$', 'update_cover_photo'),
)