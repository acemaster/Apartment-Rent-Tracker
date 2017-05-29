# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Constant(models.Model):
    """
    Description: Constant
    """
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    def __unicode__(self):
        return self.key

class Customer(models.Model):
    """
    Description: Customer 
    ======================
    check duration
    """
    user = models.OneToOneField(User)
    mobile_no = models.CharField(max_length=100)
    rent = models.CharField(max_length=100)
    total_rent_to_pay = models.CharField(max_length=100,default="0")
    def __unicode__(self):
    	return self.user.first_name

class RentPayment(models.Model):
    """
    Rent Payment with month and year
    """
    cust = models.ForeignKey(Customer)
    rent_paid = models.BooleanField(default=True)
    rent = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    month = models.CharField(max_length=100)
    def __unicode__(self):
        return self.cust.user.first_name

class Transaction(models.Model):
    """
    Description: Transaction
    Status
    """
    payment_id = models.CharField(max_length=100)
    cust = models.ForeignKey(Customer)
    create_date = models.DateTimeField(auto_now=True)
    rent_obj = models.ForeignKey(RentPayment)
    def __unicode__(self):
        return self.payment_id

