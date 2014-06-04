from django.conf.urls import patterns, include, url

import os

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
    url(r'^vestir/$', 'sistema.controller.vestir'),
	url(r'^avaliar/$', 'sistema.controller.avaliar'),
	url(r'^avaliar/(?P<id_combinacao>[0-9]+)/avaliar_combinacao$', 'sistema.controller.avaliar_combinacao'),
	url(r'^avaliar/avaliar_finalizado$', 'sistema.controller.avaliar_finalizado'),
    url(r'^guardar/$', 'sistema.controller.guardar'),
    url(r'^guardar/(?P<id_roupa>[0-9]+)/(?P<id_local>[0-9]+)/guardar_resultado$', 'sistema.controller.guardar_resultado'),
    url(r'^combinar/$', 'sistema.controller.combinar'),
    url(r'^combinar/(?P<id_combinacao>[0-9]+)/combinar_editar/$', 'sistema.controller.combinar_editar'),
    url(r'^combinar/(?P<id_combinacao>[0-9]+)/combinar_finalizado/$', 'sistema.controller.combinar_finalizado'),
    url(r'^vestir/combinacao/$', 'sistema.controller.combinacao'),
    url(r'^vestir/combinacao/(?P<id_comb>[0-9]+)/combinacao_finalizado/$' , 'sistema.controller.combinacao_finalizado'), 
    url(r'^vestir/combinacao/(?P<id_comb>[0-9]+)/recusar/$', 'sistema.controller.recusar'),
    url(r'^vestir/combinacao/(?P<itera>\w+)/retirar/$', 'sistema.controller.retirar'),
    url(r'^vestir/peca/$', 'sistema.controller.peca'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
