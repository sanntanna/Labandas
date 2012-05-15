from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^$', 'labandas.views.home'),
    (r'^login$', 'labandas.views.login'),
    (r'^logout$', 'labandas.views.logout'),
    (r'^ajax/register-musician$', 'bands.views.subscribe_musician'),
    (r'^band/create$', 'bands.views.add_band'),
    (r'^personal-info$', 'bands.views.edit_personal_info'),
     url(r'^admin/', include(admin.site.urls)),
     (r'^accounts/', include('registration.urls')),
)
