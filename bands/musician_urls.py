from django.conf.urls import patterns

urlpatterns = patterns('bands.musician_views',
    (r'^cadastrar$', 'subscribe_musician'),
    (r'^atualizar/(?P<field>[a-z_]+)$', 'update_field'),
    (r'^atualizar/(?P<obj>[a-z_]+)/(?P<attr>[a-z_]+)$', 'update_obj_field'),
    (r'^(?P<name>[a-z-]+)/(?P<user_id>\d+)$', 'public_profile'),
    (r'^(?P<name>[a-z0-9-]+)/(?P<user_id>\d+)/fotos$', 'musician_photos'),
    (r'^(?P<name>[a-z0-9-]+)/(?P<user_id>\d+)/videos$', 'musician_videos'),
    (r'^(?P<name>[a-z0-9-]+)/(?P<user_id>\d+)/bandas$', 'musician_bands'),
    (r'^(?P<name>[a-z-]+)/(?P<user_id>\d+)/mensagens$', 'all_messages'),
    (r'^buscar$', 'find_musician'),
    (r'^atualizar-imagem-perfil$', 'update_avatar'),
    (r'^atualizar-imagem-capa$', 'update_cover_photo'),
    (r'^adicionar-foto$', 'add_photo'),
    (r'^remover-foto$', 'delete_photo'),
    (r'^adicionar-video$', 'add_video'),
    (r'^remover-video$', 'delete_video'),
)