from django.contrib import admin
from backgroundsys.admin_site import admin_site
from .models import ProductWaterContent, ProductQuality, ProductTypeL2, ProductTypeL1, ProductTypeL3, ProductDemand, ProductDemandPhoto
# Register your models here.


class ProductDemandPhotoInline(admin.TabularInline):
    model = ProductDemandPhoto
    extra = 1


class ProductDemandAdmin(admin.ModelAdmin):
    inlines = [ProductDemandPhotoInline]
    list_display = ('id', '__unicode__','pid')
    list_display_links = ('id', '__unicode__','pid')


class ProductDemandPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'demand_photo', 'photo_desc')


# admin.site.register([ProductWaterContent, ProductQuality,
#                      ProductTypeL2])
admin_site.register(ProductDemand, ProductDemandAdmin)
admin_site.register(ProductDemandPhoto, ProductDemandPhotoAdmin)
