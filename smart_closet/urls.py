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
    url(r'^mala/$', 'sistema.controller.mala'),
    url(r'^guardar/$', 'sistema.controller.guardar'),
    url(r'^vestir/$', 'sistema.controller.vestir'),
    url(r'^vestir/preparo_combinacao/$', 'sistema.controller.preparar_combinacao'),#NAO ESTA FEITO
    url(r'^vestir/escolhe_peca/$', 'sistema.controller.escolhe_peca'),      # NAO ESTA FEITO
	url(r'^avaliar/$', 'sistema.controller.avaliar'),
	url(r'^avaliar/(?P<id_combinacao>[0-9]+)/avaliar_combinacao$', 'sistema.controller.avaliar_combinacao'),
	url(r'^avaliar/finalizar/$', 'sistema.controller.avaliar_finalizar'),

    
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
