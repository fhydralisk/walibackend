# coding=utf-8
from django.contrib import admin
import appraisalsys.models as appraisalsys
from django.utils.html import format_html


class ImpurityContentAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ('id', 'impcdesc', 'in_use')


class AppraisalInfoAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = (
        'ivid', 'a_status', 'in_accordance', 'description', 'net_weight', 'pure_net_weight', 'final_total_price')


class CheckPhotoAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ('uploader', 'apprid', 'upload_data', 'in_use')


to_register = [
    (appraisalsys.ImpurityContent, ImpurityContentAdmin),
    (appraisalsys.AppraisalInfo, AppraisalInfoAdmin),
    (appraisalsys.CheckPhoto, CheckPhotoAdmin),
]
