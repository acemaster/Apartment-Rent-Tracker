# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    """
    Description: Customer 
    ======================
    check duration
    """
    user = models.OneToOneField(User)
    mobile_no = models.CharField(max_length=100)
    rent_paid = models.BooleanField(default=True)
    rent = models.CharField(max_length=100)
    def __unicode__(self):
    	return self.user.first_name

