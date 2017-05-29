# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from main.models import *
import json
from django.shortcuts import redirect
import hmac
import hashlib 
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import urlparse
import datetime

# Create your views here.
def checkrent(cust,rent):
	start_year = Constant.objects.get(key="START_YEAR").value
	start_month = Constant.objects.get(key="START_MONTH").value
	now = datetime.datetime.now()
	current_year = now.year
	current_month = now.month
	calendar = {}
	total_to_pay = 0.0
	payment_dict = []
	years = ()
	for year in range(int(start_year),int(current_year)+1):
		print year
		years = years + (year,)
		calendar[str(year)] = ()
		for month in range(int(start_month),13):
			if year == current_year and month == int(current_month) + 1:
				break
			try:
				rent_payment = RentPayment.objects.get(cust=cust,year=year,month=month)
				if rent_payment.rent_paid:
					calendar[str(year)] = calendar[str(year)] + ([month,True],)
				else:
					calendar[str(year)] = calendar[str(year)] + ([month,False],)
					payment_dict.append({'year':year,'month':month,'rent':rent})
					total_to_pay = total_to_pay + float(rent)
			except:
				calendar[str(year)] = calendar[str(year)] + ([month,False],)
				payment_dict.append({'year':year,'month':month,'rent':rent})
				total_to_pay = total_to_pay + float(rent)
		start_month = 1
		print calendar[str(year)]
	return calendar,total_to_pay,payment_dict,years

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
			response['rent'] = rent
			calendar,total_to_pay,payment_dict,years = checkrent(cust,rent)
			response['total_to_pay'] = total_to_pay
			response['payment_dict'] = payment_dict
			response['calendar'] = calendar
			response['user'] = cust.user
			response['cust'] = cust
			response['years'] = years
			response['success'] = 1
		except Exception as e:
			print e
			response['message'] = "Custumer not found"
		return render(request,'main/site/confirm.djt',response)
	return render(request,'main/site/pay.djt',{})

def createpayment(request):
	cust_id = 1
	cust = Customer.objects.get(id=cust_id)
	import requests
	headers = { "X-Api-Key": "9affee63b17b104386ed8e711dfb45a6", "X-Auth-Token": "95d066dcb7b834e00cb575a0dde4a85f"}
	payload = {
	'purpose': 'Rent payment of ' + cust.user.first_name + " " + cust.user.last_name,
	'amount': str(cust.rent),
	'buyer_name': cust.user.first_name + " " + cust.user.last_name,
	'email': 'vivekhtc25@gmail.com',
	'phone': cust.mobile_no,
	'redirect_url': '/paymentconfirm',
	'send_email': 'True',
	'send_sms': 'True',
	'webhook': '/',
	'allow_repeated_payments': 'False',
	}
	response = requests.post("https://test.instamojo.com/api/1.1/payment-requests/", data=payload, headers=headers)
	result_dict = json.loads(response.text)
	if result_dict['success']:
		url = result_dict['payment_request']['longurl']
		print url
		return redirect(url)
	else:
		return render(request,'main/site/error.djt',{})

# def paymentconfirm(request):


def webhook(request):
	content_length = int(self.headers['content-length'])
	querystring = self.rfile.read(content_length)
	data = urlparse.parse_qs(querystring)
	mac_provided = data.pop('mac')
	message = "|".join(v for k, v in sorted(data.items(), key=lambda x: x[0].lower()))
	# Pass the 'salt' without the <>.
	mac_calculated = hmac.new("<YOUR_SALT>", message, hashlib.sha1).hexdigest()
	if mac_provided == mac_calculated:
		if data['status'] == "Credit":
			print "Success"
		else:
			print "Error"
		self.send_response(200)
	else:
		self.send_response(400)

