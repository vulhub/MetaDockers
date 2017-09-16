from django.conf.urls import url, handler404, handler500
from . import views

urlpatterns = [
	url(r'^info/$', views.infoRouting),
	url(r'^images', views.imageRouting),
	url(r'^index/$', views.indexRouting),
	url(r'^about/$', views.aboutRouting),
	url(r'^vulhubs/$', views.vulhubRouting),
	url(r'^volumes/$', views.volumeRouting),
	url(r'^network', views.networkRouting),
	url(r'^container', views.containerRouting),
	url(r'test', views.testRouting)
]

handler404 = views.not_found
handler500 = views.server_error