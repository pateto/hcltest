from django.conf.urls import include, patterns, url
from rango import views

urlpatterns = patterns('', url(r'^rango/', include('rango.urls')),)