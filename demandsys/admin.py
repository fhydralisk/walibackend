from django.contrib import admin

from .models import ProductWaterContent, ProductQuality, ProductTypeL2, ProductTypeL1, ProductTypeL3, ProductDemand, ProductDemandPhoto
# Register your models here.

admin.site.register([ProductWaterContent, ProductQuality, ProductTypeL2, ProductTypeL1, ProductTypeL3, ProductDemand, ProductDemandPhoto])
