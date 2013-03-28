from django.conf.urls import patterns

urlpatterns = patterns('bands.band_views',
    (r'^criar$', 'create_band'),
    (r'^atualizar-img-capa/(?P<band_id>\d+)$', 'update_cover_photo'),
    (r'^(?P<name>[a-z0-9-]+)/(?P<band_id>\d+)$', 'band_page'),
    (r'^atualizar/(?P<field>[a-z_]+)$', 'update_field'),
    (r'^atualizar/(?P<obj>[a-z_]+)/(?P<attr>[a-z_]+)$', 'update_obj_field'),
    (r'^formacao/remover$', 'remove_musician_from_band'),
)