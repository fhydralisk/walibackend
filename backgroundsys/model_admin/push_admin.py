# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import url
from django.contrib import admin
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from logsys.models import LogOrderProtocolStatus
from pushsys.models import *
from ordersys.model_choices.order_enum import o_status_choice, p_operate_status_choice
from paymentsys.models import PaymentReceipt
from logsys.models import LogOrderStatus


class JPushSecretAdmin(admin.ModelAdmin):
    list_display = ('app_key', 'upload_date', 'production')


class PushTemplateAdmin(admin.ModelAdmin):
    list_display = ('template_name', 'template', 'upload_date', 'push_state_name', 'in_use')


to_register = [
    (JPushSecret, JPushSecretAdmin),
    (PushTemplate, PushTemplateAdmin),
]
