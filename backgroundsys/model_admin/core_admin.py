# coding=utf-8
from django.contrib import admin
import coresys.models as coresys


class CityInline(admin.TabularInline):
    model = coresys.CoreAddressCity
    extra = 0


class AreaInline(admin.TabularInline):
    model = coresys.CoreAddressArea
    extra = 0


class CoreAdmin(admin.ModelAdmin):
    list_filter = ('in_use',)
    list_per_page = 30


class CoreDistributionAdmin(CoreAdmin):
    list_display = ('id', 'odmdesc', 'in_use',)
    list_display_links = ('id', 'odmdesc')
    search_fields = ('odmdesc',)


class CorePaymentAdmin(CoreAdmin):
    list_display = ('id', 'opmdesc', 'in_use',)
    list_display_links = ('id', 'opmdesc')
    search_fields = ('opmdesc',)


class CoreAddressProvinceAdmin(CoreAdmin):
    list_display = ('province', 'in_use')
    inlines = [CityInline]


class CoreAddressCityAdmin(CoreAdmin):
    list_display = ('city', 'pid', 'in_use')
    list_display_links = ('city',)
    inlines = [AreaInline]

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ('pid',)
        return self.readonly_fields


class CoreAddressAreaAdmin(CoreAdmin):
    list_display = ('area', 'province', 'cid', 'in_use',)
    list_display_links = ('area',)

    def province(self, obj):
        return obj.cid.pid

    province.short_description = "所属省"

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (('area',), ('in_use',), ('province',), ('cid',),)
            }),
        )
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ('province', 'cid',)
        return self.readonly_fields


to_register = [
    (coresys.CoreAddressProvince, CoreAddressProvinceAdmin),
    (coresys.CoreAddressArea, CoreAddressAreaAdmin),
    (coresys.CoreAddressCity, CoreAddressCityAdmin),
]
