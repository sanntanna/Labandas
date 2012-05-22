from bands.views import SubscribeMusician, EditMusician, UpdateCep, AddBand, \
    MusicianProfile, BandPage, EditBand
from django.conf.urls import patterns, include, url
from django.contrib import admin
from solicitations.views import SolicitationMusician

admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^$', 'labandas.views.home'),
    (r'^login$', 'labandas.views.login'),
    (r'^logout$', 'labandas.views.logout'),
    (r'^musico/cadastrar$', SubscribeMusician()),
    (r'^musico/atualizar-endereco$', UpdateCep()),
    (r'^musico/editar$', EditMusician()),
    (r'^musico/(?P<name>[a-z-]+)/(?P<user_id>\d+)$', MusicianProfile()),
    (r'^musico/bandas$', 'bands.views.get_bands'),
    (r'^banda/cadastrar$', AddBand()),
    (r'^banda/editar/(?P<band_id>\d+)$', EditBand()),
    (r'^banda/(?P<name>[a-z-]+)/(?P<band_id>\d+)$', BandPage()),
    (r'^equipamentos/instrumentos$', 'equipaments.views.get_instruments'),
    (r'^solicitacao/musico/enviar$', SolicitationMusician()),
     url(r'^admin/', include(admin.site.urls)),
     (r'^accounts/', include('registration.urls')),
)
