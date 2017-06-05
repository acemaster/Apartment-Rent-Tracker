from django.conf.urls import include, url
from owner import views

urlpatterns = [
	url(r'^$',views.home),
	url(r'^signin/$',views.signin),
	url(r'^signout/$',views.signout),
	url(r'^getcustinfo/(?P<cust_id>[A-Za-z0-9.-]+)$',views.getcustinfo),
	url(r'^addcust/$',views.addcust),
]