# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from main.models import *

# Register your models here.


admin.site.register(Customer)
admin.site.register(Constant)
admin.site.register(RentPayment)
admin.site.register(Transaction)