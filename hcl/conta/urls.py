from django.conf.urls import patterns, url
from conta import views

urlpatterns = patterns(
		'',
        url(r'^$', views.index, name='index'),
		url(r'^hoja_de_vida/1$', views.hoja_de_vida, name='hoja_de_vida'),
		url(r'^hoja_de_vida/$', views.hoja_de_vida_pag, name='hoja_de_vida_pag'),
	)