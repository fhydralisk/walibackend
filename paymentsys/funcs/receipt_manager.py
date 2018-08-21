"""

"""
import uuid
from django.utils.module_loading import import_string
from django.conf import settings
from base.exceptions import WLException
from paymentsys.model_choices.receipt_enum import receipt_status_choice, receipt_type_choice
from paymentsys.models import PaymentReceipt, PaymentPlatform


class AbstractReceiptCallback(object):

    def pay_confirm(self, order, context):
        raise NotImplementedError

    def refund_confirm(self, order, context):
        raise NotImplementedError


class AbstractReceiptManager(object):

    def generate(self, order, r_type, amount, context):
        raise NotImplementedError

    def respond_receipt(self, receipt, response):
        raise NotImplementedError

    def get_callback(self):
        str_callback_class = settings.PAYMENT["RECEIPT_MANAGER"]["CALLBACK"]
        callback = import_string(str_callback_class)  # type: AbstractReceiptCallback
        return callback


class DummyReceiptManager(AbstractReceiptManager):
    def generate(self, order, r_type, amount, context):

        # if r_type in ( receipt_type_choice.FINAL_PAYMENT):
        #     self.callback.pay_confirm(order, None)
        # else:
        #     self.callback.refund_confirm(order, None)

        if r_type in receipt_type_choice.FINAL_REFUND:
            rs = receipt_status_choice.WAIT_REFUND
            r_type_payment = (
                receipt_type_choice.FINAL_PAYMENT
            )
            try:
                related_payment = PaymentReceipt.objects.get(
                    oid=order,
                    receipt_status=receipt_status_choice.PAYED,
                    receipt_type=r_type_payment
                )
                platform = related_payment.ppid
            except (PaymentReceipt.DoesNotExist, PaymentReceipt.MultipleObjectsReturned):
                raise AssertionError("Multiple or None related payment")
        else:
            rs = receipt_status_choice.WAIT_PAYMENT
            platform = PaymentPlatform.objects.get(id=context["paymethod"])

        PaymentReceipt.objects.create(
            receipt_type=r_type,
            receipt_status=rs,
            ppid=platform,
            receipt_number=str(uuid.uuid1()),
            sum=amount,
            oid=order
        )

    def respond_receipt(self, receipt, response):
        # type: (PaymentReceipt, dict) -> None
        if response["r_type"] == "refund":
            if receipt.receipt_status != receipt_status_choice.WAIT_REFUND:
                raise WLException(400, "Unexpected receipt status")
            receipt.receipt_status = receipt_status_choice.REFUNDED
            receipt.save()
            self.get_callback().refund_confirm(response["oid"], None)
        else:
            if receipt.receipt_status not in (
            receipt_status_choice.WAIT_PAYMENT, receipt_status_choice.NOT_PAYED_WAIT_PLATFORM):
                raise WLException(400, "Unexpected receipt status")
            receipt.receipt_status = receipt_status_choice.PAYED
            receipt.save()
            self.get_callback().pay_confirm(response["oid"], None)


manager = import_string(settings.PAYMENT["RECEIPT_MANAGER"]["CLASS"])(
    **settings.PAYMENT["RECEIPT_MANAGER"].get("ARGS", {})
)  # type: AbstractReceiptManager
