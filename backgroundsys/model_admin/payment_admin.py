# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import url
from django.contrib import admin
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from logsys.models import LogOrderProtocolStatus
from paymentsys.models import *
from ordersys.model_choices.order_enum import o_status_choice, p_operate_status_choice
from logsys.models import LogOrderStatus


class PaymentPlatformAdmin(admin.ModelAdmin):
    # ordering = ('-id',)
    list_display = ('description','module','in_use')


class PaymentReceiptAdmin(admin.ModelAdmin):
    list_display = ('oid','ppid','receipt_number','receipt_type','receipt_status','sum','platform_number')


to_register = [
    (PaymentPlatform, PaymentPlatformAdmin),
    (PaymentReceipt, PaymentReceiptAdmin),
]
