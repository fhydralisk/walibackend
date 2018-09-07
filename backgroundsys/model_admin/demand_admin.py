# coding=utf-8
from django.contrib import admin
import demandsys.models as demandsys


class ProductTypeL2Inline(admin.TabularInline):
    model = demandsys.ProductTypeL2
    extra = 0

    class Meta:
        verbose_name = "包含的二级种类"
        verbose_name_plural = verbose_name


class DemandAdmin(admin.ModelAdmin):
    list_per_page = 10


class ProductTypeL3Admin(DemandAdmin):
    list_display = ('id', 'tname1', 'tname2', 'tname3')

    def tname2(self, obj):
        return obj.t2id.tname2

    tname2.short_description = "所属二级类型"

    def tname1(self, obj):
        return obj.t2id.t1id.tname1

    tname1.short_description = "所属一级类型"


class ProductTypeL1Admin(DemandAdmin):
    list_display = ('id', 'tname1', 'in_use')
    inlines = [ProductTypeL2Inline]


class ProductTypeL2Admin(DemandAdmin):
    list_display = ('t1id', 'tname2', 'in_use')


class ProductWaterContentAdmin(DemandAdmin):
    list_display = ('pwcdesc', 'ord', 'in_use')


class ProductQualityAdmin(DemandAdmin):
    list_display = ('pqdesc', 'ord', 't3id', 'in_use')


class ProductDemandPhotoInline(admin.TabularInline):
    model = demandsys.ProductDemandPhoto
    extra = 1


class ProductDemandAdmin(admin.ModelAdmin):
    inlines = [ProductDemandPhotoInline]
    list_display = ('id', '__unicode__', 'uid', 'st_time', 'end_time', 'comment', 'match', 'create_datetime', 'in_use')
    list_display_links = ('id', '__unicode__')


class ProductDemandPhotoAdmin(admin.ModelAdmin):
    list_display = ('dmid', 'photo_desc', 'demand_photo', 'demand_photo_snapshot', 'upload_date',)


to_register = [
    (demandsys.ProductTypeL3, ProductTypeL3Admin),
    (demandsys.ProductTypeL1, ProductTypeL1Admin),
    (demandsys.ProductTypeL2, ProductTypeL2Admin),
    (demandsys.ProductQuality, ProductQualityAdmin),
    (demandsys.ProductWaterContent, ProductWaterContentAdmin),
    (demandsys.ProductDemand, ProductDemandAdmin),
    (demandsys.ProductDemandPhoto, ProductDemandPhotoAdmin),
]
