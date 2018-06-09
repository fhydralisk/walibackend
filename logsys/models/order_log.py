from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from usersys.models import UserBase
from ordersys.model_choices.order_enum import o_status_choice, p_operate_status_choice, p_status_choice
from ordersys.models import OrderInfo, OrderProtocol


class LogOrderStatus(models.Model):
    oid = models.ForeignKey(
        OrderInfo,
        verbose_name=_("Order"),
        related_name="order_log",
        on_delete=models.CASCADE,
    )
    operator = models.ForeignKey(
        UserBase,
        blank=True,
        null=True,
    )
    log_date_time = models.DateTimeField(auto_now_add=True)
    o_status = models.IntegerField(choices=o_status_choice.choice)
    context = models.TextField(blank=True, null=True)


class LogOrderProtocolStatus(models.Model):
    opid = models.ForeignKey(
        OrderProtocol,
        verbose_name=_("OrderProtocol"),
        related_name="order_protocol_log",
        on_delete=models.CASCADE
    )
    operator = models.ForeignKey(
        UserBase,
        blank=True,
        null=True,
    )
    log_date_time = models.DateTimeField(auto_now_add=True)
    p_status = models.IntegerField(choices=p_status_choice.choice)
    p_operate_status = models.IntegerField(choices=p_operate_status_choice.choice)
    context = models.TextField(blank=True, null=True)
