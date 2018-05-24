"""

"""
import uuid
from django.utils.module_loading import import_string
from django.conf import settings
from paymentsys.models.receipt_enum import receipt_status_choice
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

        # if r_type in (receipt_type_choice.EARNEST_PAYMENT, receipt_type_choice.FINAL_PAYMENT):
        #     self.callback.pay_confirm(order, None)
        # else:
        #     self.callback.refund_confirm(order, None)

        PaymentReceipt.objects.create(
            receipt_type=r_type,
            receipt_status=receipt_status_choice.WAIT_PAYMENT,
            ppid=PaymentPlatform.objects.get(id=context["paymethod"]),
            receipt_number=str(uuid.uuid1()),
            sum=amount,
            oid=order
        )

    def respond_receipt(self, receipt, response):
        if response["r_type"] == "refund":
            self.get_callback().refund_confirm(response["oid"], None)
        else:
            self.get_callback().pay_confirm(response["oid"], None)


manager = import_string(settings.PAYMENT["RECEIPT_MANAGER"]["CLASS"])(
    **settings.PAYMENT["RECEIPT_MANAGER"].get("ARGS", {})
)  # type: AbstractReceiptManager
