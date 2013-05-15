from django.conf.urls import patterns

urlpatterns = patterns('bands.band_views',
    (r'^criar$', 'create_band'),
    (r'^criar-post$', 'create_band_post'),
    (r'^atualizar-img-capa/(?P<band_id>\d+)$', 'update_cover_photo'),
    (r'^(?P<name>[a-z0-9-]+)/(?P<band_id>\d+)$', 'band_page'),
    (r'^(?P<name>[a-z0-9-]+)/(?P<band_id>\d+)/setlist$', 'band_setlist'),
    (r'^(?P<name>[a-z0-9-]+)/(?P<band_id>\d+)/fotos$', 'band_photos'),
    (r'^(?P<name>[a-z0-9-]+)/(?P<band_id>\d+)/videos$', 'band_videos'),
    (r'^(?P<name>[a-z0-9-]+)/(?P<band_id>\d+)/historico-de-anuncios$', 'band_history_ads'),    
    (r'^atualizar/setlist$', 'update_setlist'),
    (r'^remover/setlist$', 'remove_music_from_setlist'),
    (r'^atualizar/(?P<field>[a-z_]+)$', 'update_field'),
    (r'^atualizar/(?P<obj>[a-z_]+)/(?P<attr>[a-z_]+)$', 'update_obj_field'),
)