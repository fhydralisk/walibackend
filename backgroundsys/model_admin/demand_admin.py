# coding=utf-8
from django.contrib import admin
import demandsys.models as demandsys
from django.utils.html import format_html


class ProductTypeL2Inline(admin.TabularInline):
    model = demandsys.ProductTypeL2
    extra = 0


class DemandAdmin(admin.ModelAdmin):
    list_per_page = 10
    ordering = ('id',)


class ProductTypeL3Admin(DemandAdmin):
    list_display = ('id', 'tname1', 'tname2', 'tname3')

    def tname2(self, obj):
        return obj.t2id.tname2

    tname2.short_description = "二级货物类型"

    def tname1(self, obj):
        return obj.t2id.t1id.tname1

    tname1.short_description = "一级货物类型"


class ProductTypeL1Admin(DemandAdmin):
    list_display = ('id', 'tname1', 'button')
    readonly_fields = ("button",)
    inlines = [ProductTypeL2Inline]

    def button(self, obj):
        return format_html('<button type="button" onclick="alert(\'hello world!\')">点我!</button>')


class ProductTypeL2Admin(DemandAdmin):
    list_display = ('t1id', 'tname2', 'in_use')


class ProductWaterContentAdmin(DemandAdmin):
    list_display = ('pwcdesc', 'ord', 'in_use')


class ProductQualityAdmin(DemandAdmin):
    list_display = ('pqdesc', 'ord', 't3id', 'in_use')


# admin.site.register([ProductWaterContent, ProductQuality,
#                      ProductTypeL2])
to_register = [
    (demandsys.ProductTypeL3, ProductTypeL3Admin),
    (demandsys.ProductTypeL1, ProductTypeL1Admin),
    (demandsys.ProductTypeL2, ProductTypeL2Admin),
    (demandsys.ProductQuality,ProductQualityAdmin),
    (demandsys.ProductWaterContent,ProductWaterContentAdmin),
]
