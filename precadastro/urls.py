from django.conf.urls import patterns

urlpatterns = patterns('precadastro.views',
    (r'^em-breve$', 'landing_page'),
    (r'^salvar$', 'landing_page_submit'),
)