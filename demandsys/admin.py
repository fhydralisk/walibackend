from django.contrib import admin

from .models import ProductWaterContent, ProductQuality, ProductTypeL2, ProductTypeL1, ProductTypeL3, ProductDemand, ProductDemandPhoto
# Register your models here.


class ProductDemandPhotoInline(admin.TabularInline):
    model = ProductDemandPhoto
    extra = 1


class ProductDemandAdmin(admin.ModelAdmin):
    inlines = [ProductDemandPhotoInline]
    list_display = ('id', '__unicode__')
    list_display_links = ('id', '__unicode__')


admin.site.register([ProductWaterContent, ProductQuality,
                     ProductTypeL2, ProductTypeL1, ProductTypeL3, ProductDemandPhoto])
admin.site.register(ProductDemand, ProductDemandAdmin)
