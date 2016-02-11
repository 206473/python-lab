from django.conf.urls import url

from . import views

urlpatterns = [
	url('subscription/$', views.subscription),
	url(r'main/$', views.main),
	url(r'ViewImages/$', views.ViewImages),
	
]