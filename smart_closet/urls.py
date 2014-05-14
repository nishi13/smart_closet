from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'sistema.controller.home'),
    url(r'^configurar/$', 'sistema.controller.configurar'),
    url(r'^configurar/roupa/$', 'sistema.controller.config_roupa'),
    url(r'^configurar/roupa/incluir$', 'sistema.controller.roupa_incluir'),
    url(r'^configurar/armario/$', 'sistema.controller.config_armario'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
