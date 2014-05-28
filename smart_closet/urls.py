from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'sistema.controller.home'),
    url(r'^configurar/$', 'sistema.controller.configurar'),
    url(r'^configurar/roupa/$', 'sistema.controller.config_roupa'),
    url(r'^configurar/armario/$', 'sistema.controller.config_armario'),
    url(r'^configurar/roupa/(?P<id_roupa>[0-9]+)/incluirRDIF$', 'sistema.controller.roupa_incluir_RFID'),
    url(r'^configurar/roupa/(?P<id_roupa>[0-9]+)/local$', 'sistema.controller.roupa_incluir_local'),
    url(r'^avaliar/$', 'sistema.controller.avaliar'),
    url(r'^mala/$', 'sistema.controller.mala'),
    url(r'^guardar/$', 'sistema.controller.guardar'),
    url(r'^vestir/$', 'sistema.controller.vestir'),
    url(r'^vestir/combinacao/$', 'sistema.controller.combinacao'),#NAO ESTA FEITO
    url(r'^vestir/peca/$', 'sistema.controller.peca'),      # NAO ESTA FEITO

    
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
