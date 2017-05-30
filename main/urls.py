from django.conf.urls import include, url
from main import views

urlpatterns = [
	url(r'^$',views.home),
	url(r'^payrent/$',views.payrent),
	url(r'^startpayment/(?P<cust_id>[A-Za-z0-9.-]+)$',views.createpayment),
]