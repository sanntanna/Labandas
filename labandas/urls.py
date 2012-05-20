from bands.views import SubscribeMusician, EditMusician, UpdateCep, AddBand, \
    MusicianProfile
from django.conf.urls import patterns, include, url
from django.contrib import admin

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
    (r'^musico/(?P<name>[a-z-]+)/(?P<uid>\d+)$', MusicianProfile()),
    (r'^banda/cadastrar$', AddBand()),
     url(r'^admin/', include(admin.site.urls)),
     (r'^accounts/', include('registration.urls')),
)
