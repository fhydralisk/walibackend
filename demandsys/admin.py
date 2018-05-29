from django.contrib import admin

from .models import ProductWaterContent, ProductQuality, ProductTypeL2, ProductTypeL1, ProductTypeL3, ProductDemand, ProductDemandPhoto
# Register your models here.


class ShowIdAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register([ProductWaterContent, ProductQuality, ProductTypeL2, ProductTypeL1, ProductTypeL3, ProductDemandPhoto])
admin.site.register(ProductDemand, ShowIdAdmin)
