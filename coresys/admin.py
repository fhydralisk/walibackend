from django.contrib import admin
from backgroundsys.admin_site import admin_site
from django.db import models
from coresys.models import CoreDistributionMethod, CorePaymentMethod, CoreAddressCity, CoreAddressProvince, \
    CoreAddressArea


# Register your models here.


# admin.site.register(
#     [CoreAddressProvince, CoreAddressCity, CoreAddressArea, CoreDistributionMethod, CorePaymentMethod, ])
#
# admin.site.register(
#     [CoreAddressProvince, CoreAddressCity, CoreAddressArea, ])
