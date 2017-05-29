from django.conf.urls import include, url
from main import views

urlpatterns = [
	url(r'^$',views.home),
	url(r'^payrent/$',views.payrent),
	url(r'^startpayment/$',views.createpayment),
]