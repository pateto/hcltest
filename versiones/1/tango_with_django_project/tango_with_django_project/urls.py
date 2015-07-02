from django.conf import settings
from django.conf.urls import include, patterns, url
from rango import views
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^rango/', include('rango.urls', namespace='rango')),
	url(r'^accounts/', include('registration.backends.simple.urls')),
	)

if settings.DEBUG:
	urlpatterns += patterns('django.views.static',(r'^media/(?P<path>.*)','serve',{'document_root': settings.MEDIA_ROOT}), )