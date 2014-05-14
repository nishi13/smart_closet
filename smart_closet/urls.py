from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'sistema.controller.home'),
    url(r'^configurar/$', 'sistema.controller.configurar'),
    url(r'^configurar/roupa/$', 'sistema.controller.config_roupa'),
    url(r'^configurar/roupa/(?P<id_roupa>[0-9]+)/incluirRDIF$', 'sistema.controller.roupa_incluir_RFID'),
    url(r'^configurar/roupa/(?P<id_roupa>[0-9]+)/local$', 'sistema.controller.roupa_incluir_local'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
