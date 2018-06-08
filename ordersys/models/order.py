from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from base.util.statemachine import ActionBasedStateMachineMixin
from invitesys.models import InviteInfo

from ordersys.model_choices.order_enum import o_status_choice, op_type_choice, p_status_choice, p_operate_status_choice
from ordersys.statemachine.order_sm import OrderInfoStateMachinDef
from ordersys.statemachine.order_protocol_sm import OrderProtocolStateMachineDef


class OrderInfo(models.Model, ActionBasedStateMachineMixin):
    ivid = models.OneToOneField(
        InviteInfo,
        verbose_name=_("Invite"),
        on_delete=models.CASCADE,
        related_name="invite_order"
    )
    o_status = models.IntegerField(_("order status"), choices=o_status_choice.choice)
    final_price = models.FloatField(null=True, blank=True)

    o_status_sm = OrderInfoStateMachinDef(attr='o_status')

    @property
    def current_protocol(self):
        return self.order_protocol.exclude(
            p_status__in={p_status_choice.REJECTED, p_status_choice.EXECUTED, p_status_choice.CANCELED}
        ).get()

    @property
    def current_receipt(self):
        from paymentsys.models import PaymentReceipt

        return self.order_receipt.exclude(
            receipt_status__in=PaymentReceipt.current_status_set()
        ).get()

    @property
    def buyer_invoice_info(self):
        return self.ivid.buyer.user_validate

    def __unicode__(self):
        return "Order from %s" % str(self.ivid)


class OrderProtocol(models.Model, ActionBasedStateMachineMixin):
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

    p_operate_status_sm = OrderProtocolStateMachineDef(attr='p_operate_status')

    @property
    def terminated(self):
        return self.p_status in (p_status_choice.REJECTED, p_status_choice.EXECUTED, p_status_choice.CANCELED)

    def init_p_operate_status(self):
        map_optype_pops = {
            op_type_choice.CANCEL: p_operate_status_choice.CANCEL_WAIT_RETURN,
            op_type_choice.NORMAL: p_operate_status_choice.NORMAL_WAIT_FINAL,
        }
        if self.op_type == op_type_choice.ADJUST_PRICE:

            self.p_operate_status = (
                p_operate_status_choice.ADJUST_WAIT_FINAL
                if self.c_price > self.oid.ivid.earnest
                else p_operate_status_choice.ADJUST_CHECK_EARNEST
                if self.c_price < self.oid.ivid.earnest
                else p_operate_status_choice.ADJUST_OK
            )

        else:
            self.p_operate_status = map_optype_pops[self.op_type]
