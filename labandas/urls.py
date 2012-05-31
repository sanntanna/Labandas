from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^$', 'labandas.views.home'),
    (r'^login$', 'labandas.views.login'),
    (r'^logout$', 'labandas.views.logout'),
    (r'^equipamentos/instrumentos$', 'equipaments.views.get_instruments'),
    url(r'^solicitacao/', include('solicitations.urls')),
    url(r'^musico/', include('bands.musician_urls')),
    url(r'^banda/', include('bands.band_urls')),
    url(r'^admin/', include(admin.site.urls)),
)
