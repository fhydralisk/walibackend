# coding=utf-8
from django.contrib import admin
import appraisalsys.models as appraisalsys
from django.utils.html import format_html
from simple_history.admin import SimpleHistoryAdmin
from django.core.urlresolvers import reverse


class ImpurityContentAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ('id', 'impcdesc', 'in_use')


class AppraisalInfoAdmin(SimpleHistoryAdmin):
    list_per_page = 30
    list_display = (
        'ivid', 'a_status', 'in_accordance', 'parameter', 'net_weight', 'pure_net_weight', 'final_total_price','operate')
    history_list_display = ['change_reason', 'change_comment', ]

    def operate(self, obj):
        history = '历史'
        history_url = reverse('backgroundsys:appraisalsys_appraisalinfo_history', args=(obj.id,))

        return format_html(
            '<a href="{}">{}</a> '.format(history_url, history))

    operate.short_description = '操作'


class CheckPhotoAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ('uploader', 'apprid', 'upload_data', 'in_use')


to_register = [
    (appraisalsys.ImpurityContent, ImpurityContentAdmin),
    (appraisalsys.AppraisalInfo, AppraisalInfoAdmin),
    (appraisalsys.CheckPhoto, CheckPhotoAdmin),
]
