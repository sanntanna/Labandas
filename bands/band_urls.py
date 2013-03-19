from django.conf.urls import patterns

urlpatterns = patterns('bands.band_views',
    (r'^criar$', 'create_band'),
    (r'^atualizar-img-capa/(?P<band_id>\d+)$', 'update_cover_photo'),
    (r'^(?P<name>[a-z0-9-]+)/(?P<band_id>\d+)$', 'band_page'),
    (r'^formacao/remover$', 'remove_musician_from_band'),
)