from django.contrib import admin
import coresys.models as coresys


class CoreAdmin(admin.ModelAdmin):
    list_filter = ('in_use', )
    list_editable = ('in_use', )


class CoreDistributionAdmin(CoreAdmin):
    list_display = ('id', 'odmdesc', 'in_use',)
    list_display_links = ('id', 'odmdesc')
    search_fields = ('odmdesc', )


class CorePaymentAdmin(CoreAdmin):

    list_display = ('id', 'opmdesc', 'in_use', )
    list_display_links = ('id', 'opmdesc')
    search_fields = ('opmdesc', )


to_register = [
    (coresys.CorePaymentMethod, CorePaymentAdmin),
    (coresys.CoreDistributionMethod, CoreDistributionAdmin),
]
