from django.conf import settings
from django.utils.module_loading import import_string
from paymentsys.model_choices.receipt_enum import receipt_type_choice


# TODO: Calculate the amount of money
class AbstractReceiptCalculator(object):
    @staticmethod
    def cal_order_receipt_amount(order, r_type, ctx):
        raise NotImplementedError


class DummyReceiptCalculator(AbstractReceiptCalculator):
    @staticmethod
    def cal_order_receipt_amount(order, r_type, ctx):
        from ordersys.models import OrderInfo
        # type: (OrderInfo, int, dict) -> float
        iv = order.ivid

        if r_type == receipt_type_choice.EARNEST_PAYMENT:
            return iv.earnest
        elif r_type == receipt_type_choice.FINAL_PAYMENT:
            # Check if the price is adjusted
            if ctx.get("with_adjustment", False):
                adjusted_price = order.current_protocol.c_price
                return iv.final_price - (iv.total_price - adjusted_price)
            else:
                return iv.final_price
        elif r_type == receipt_type_choice.EARNEST_REFUND:
            if ctx.get("with_adjustment", False):
                adjusted_price = order.current_protocol.c_price
                return iv.earnest - adjusted_price
            else:
                return iv.earnest


receipt_calculator = import_string(
    settings.CALCULATOR["RECEIPT"]
)  # type: AbstractReceiptCalculator
