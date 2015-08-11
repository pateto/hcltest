from django.conf.urls import include, patterns, url
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^', include('conta.urls', namespace='conta')),
	url(r'^admin/', include(admin.site.urls)),	
	)