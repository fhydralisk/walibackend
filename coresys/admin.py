from django.contrib import admin

from coresys.models import CoreDistributionMethod, CorePaymentMethod, CoreAddressCity, CoreAddressProvince, CoreAddressArea
# Register your models here.

admin.site.register([CoreAddressProvince, CoreAddressCity, CoreAddressArea, CoreDistributionMethod, CorePaymentMethod,])
