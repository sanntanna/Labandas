from django.conf.urls import patterns

urlpatterns = patterns('bands.band_views',
    (r'^cadastrar$', 'add_band'),
    (r'^cadastrar/post$', 'add_band_post'),
    (r'^editar/(?P<band_id>\d+)$', 'edit_band'),
    (r'^editar/(?P<band_id>\d+)/post$', 'edit_band_post'),
    (r'^(?P<name>[a-z0-9-]+)/(?P<band_id>\d+)$', 'band_page'),
    (r'^formacao/remover$', 'remove_musician_from_band'),
)