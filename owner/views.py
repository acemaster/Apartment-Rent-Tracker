# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from main.models import *
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404,JsonResponse
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Sum,Q
from main.views import checkrent

# Create your views here.
message_newuser = "Hi {name}\nThanks for Apartment Registeration. Your password is {password} and your mobile number is {number}. Your rent is {rent}. Go to http://139.59.70.200/payrent/ to get your bill"

def sendsms(message,cust):
	payload = (
	('authkey',settings.SMS_INFO['auth_key']),
	('password',settings.SMS_INFO['password']),
	('message',message),
	('from',settings.SMS_INFO['from']),
	('mobile',cust_id.mobile_no))
	url="http://bulk.rocktwosms.com/spanelv2/api.php"
	r = requests.get(url,params=payload)
	print r.text
	print r.url

@login_required(login_url='/adminpanel/signin/')
def home(request):
	response={}
	earnings = RentPayment.objects.filter(rent_paid=True).aggregate(total_rent_recv=Sum('rent'))['total_rent_recv']
	customers = Customer.objects.all()
	customers_not_paid = Customer.objects.filter(~Q(total_rent_to_pay="0"))
	response['earnings'] = earnings
	response['customers'] = customers
	response['customers_not_paid'] = customers_not_paid
	return render(request,'owner/site/home.djt',response)

@login_required(login_url='/adminpanel/signin/')
def getcustinfo(request,cust_id):
	response = {}
	response['success'] = False
	try:
		cust = Customer.objects.get(id = cust_id)
		rent = cust.rent
		response['rent'] = rent
		calendar,total_to_pay,payment_dict,years = checkrent(cust,rent)
		response['total_to_pay'] = total_to_pay
		response['payment_dict'] = payment_dict
		response['calendar'] = calendar
		response['user'] = cust.user
		response['cust'] = cust
		response['years'] = years
		response['success'] = True
	except Exception as e:
		print e
	return render(request,'owner/site/custinfo.djt',response)

def signin(request):
	response={}
	if request.user.is_authenticated():
	    return redirect('/adminpanel/signin/')
	if request.method == "POST":
	    username = request.POST['username']
	    password = request.POST['password']
	    user = authenticate(username=username, password=password)
	    if user is not None:
	        login(request, user)
	        return redirect('/adminpanel/')
	    else:
	        response['message']='User is not registered / Password Incorrect' 
	return render(request,'owner/site/login.djt',response)

@login_required(login_url='/adminpanel/signin/')
def signout(request):
	logout(request)
	return redirect('/')

@login_required(login_url='/adminpanel/signin/')
def addcust(request):
	if request.method == 'POST':
		name = request.POST['name']
		email = request.POST['email']
		mobile_no = request.POST['mobile_no']
		rent = request.POST['rent']
		names = name.split(" ")
		first_name = names[0]
		last_name = names[1] if len(names)>1 else ""
		user = User()
		user.first_name = first_name
		user.last_name = last_name
		user.email = email
		user.username = email
		password = User.objects.make_random_password()
		user.set_password(password)
		user.save()
		c = Customer()
		c.user = user
		c.mobile_no = mobile_no
		c.rent = rent
		c.save()
		calendar,total_to_pay,payment_dict,years = checkrent(c,rent)
		c.total_rent_to_pay = total_to_pay
		c.save()
		return HttpResponseRedirect('/adminpanel/')
	return render(request,'owner/site/addcust.djt',{})
