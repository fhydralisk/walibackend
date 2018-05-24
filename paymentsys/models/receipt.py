from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from ordersys.models import OrderInfo
from .receipt_enum import receipt_status_choice, receipt_type_choice
from .platform import PaymentPlatform


class PaymentReceipt(models.Model):
    oid = models.ForeignKey(
        OrderInfo,
        related_name="order_receipt",
        db_index=True,
        verbose_name=_("Order")
    )
    ppid = models.ForeignKey(
        PaymentPlatform,
        db_index=False,
        verbose_name=_("Platform")
    )
    receipt_number = models.CharField(max_length=256, db_index=True, unique=True)
    receipt_type = models.IntegerField(choices=receipt_type_choice.choice)
    receipt_status = models.IntegerField(choices=receipt_status_choice.choice)
    sum = models.FloatField()
    platform_number = models.CharField(max_length=256, db_index=True, unique=True, blank=True, null=True)
    context = models.TextField(blank=True, null=True)

    def is_finished(self):
        return self.receipt_status in {receipt_status_choice.PAYED, receipt_status_choice.REFUNDED}

    def is_refunding(self):
        return self.receipt_status in {receipt_status_choice.WAIT_REFUND, } or (
            self.receipt_type in {receipt_type_choice.FINAL_REFUND, receipt_type_choice.EARNEST_REFUND}
            and self.receipt_status in {receipt_status_choice.WAIT_PAYMENT, }
        )

    def can_not_change(self):
        return self.receipt_status not in {
            receipt_status_choice.WAIT_PAYMENT,
            receipt_status_choice.NOT_PAYED_WAIT_PLATFORM,
        }

    @staticmethod
    def current_status_set():
        return {
            receipt_status_choice.PAYED,
            receipt_status_choice.REFUNDED,
            receipt_status_choice.CANCELED
        }

    def __unicode__(self):
        type_value = ""
        for choice_value, choice_name in receipt_type_choice.choice:
            if choice_value == self.receipt_type:
                type_value = choice_name
                break
        return "Receipt of %s, sum: %s, type: %s" % (self.oid, self.sum, type_value)
