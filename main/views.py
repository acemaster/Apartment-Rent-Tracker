# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from main.models import *

# Create your views here.


def home(request):
	return render(request,'main/layout/home.djt',{})

def payrent(request):
	response = {}
	response['success'] = 0
	if request.method == 'POST':
		mobile_no = request.POST['mobile_no']
		try:
			cust = Customer.objects.get(mobile_no = mobile_no)
			rent = cust.rent
			paid = cust.rent_paid
			response['rent'] = rent
			response['is_rent_paid'] = paid
			response['user'] = cust.user
			response['cust'] = cust
			response['success'] = 1
		except:
			response['message'] = "Custumer not found"
		return render(request,'main/site/confirm.djt',response)
	return render(request,'main/site/pay.djt',{})