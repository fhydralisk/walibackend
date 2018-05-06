from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from invitesys.models import InviteInfo

from .order_enum import o_status_choice, op_type_choice, p_status_choice, p_operate_status_choice


class OrderInfo(models.Model):
    ivid = models.ForeignKey(
        InviteInfo,
        verbose_name=_("Invite"),
        on_delete=models.PROTECT,
        related_name="invite_order"
    )
    o_status = models.IntegerField(_("order status"), choices=o_status_choice.choice)
    final_price = models.FloatField(null=True, blank=True)


class OrderProtocol(models.Model):
    oid = models.ForeignKey(
        OrderInfo,
        verbose_name=_("Order"),
        on_delete=models.CASCADE,
        related_name="order_protocol"
    )
    op_type = models.IntegerField(_("protocol type"), choices=op_type_choice.choice)
    p_status = models.IntegerField(_("protocol type"), choices=p_status_choice.choice)
    p_operate_status = models.IntegerField(_("protocol type"), choices=p_operate_status_choice.choice)
    c_price = models.FloatField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    op_datetime = models.DateTimeField(auto_now_add=True)
