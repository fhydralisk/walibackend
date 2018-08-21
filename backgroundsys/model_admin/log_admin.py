# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import url
from django.contrib import admin
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from logsys.models import LogOrderProtocolStatus
from ordersys.models import *
from ordersys.model_choices.order_enum import o_status_choice, p_operate_status_choice
from paymentsys.models import PaymentReceipt
from logsys.models import LogOrderStatus
import parameter as para


class LogOrderStatusAdmin(admin.ModelAdmin):
    # ordering = ('-id',)
    list_display = ('oid', 'operator', 'log_date_time', 'o_status')


class LogOrderProtocolStatusAdmin(admin.ModelAdmin):
    list_display = ('opid', 'operator', 'log_date_time', 'p_status', 'p_operate_status')


to_register = [
    (LogOrderProtocolStatus, LogOrderProtocolStatusAdmin),
    (LogOrderStatus, LogOrderStatusAdmin),
]
