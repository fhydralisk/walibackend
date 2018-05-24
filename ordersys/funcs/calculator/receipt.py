from django.conf import settings
from django.utils.module_loading import import_string


# TODO: Calculate the amount of money
class AbstractReceiptCalculator(object):
    @staticmethod
    def cal_order_receipt_amount(order, r_type):
        raise NotImplementedError


class DummyReceiptCalculator(AbstractReceiptCalculator):
    @staticmethod
    def cal_order_receipt_amount(order, r_type):
        return 0


receipt_calculator = import_string(
    settings.CALCULATOR["RECEIPT"]
)  # type: AbstractReceiptCalculator
