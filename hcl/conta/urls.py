from django.conf.urls import patterns, url
from conta import views

urlpatterns = patterns(
		'',
        url(r'^$', views.index, name='index'),
		# ex: /nhva01/1/
		url(r'^nhva01/(?P<nhva01_id>[0-9]+)/$', views.nhva01_detail, name='nhva01_detail'),
		url(r'^nhva01/$', views.nhva01, name='nhva01'),
	)