from django.conf import settings
from django.utils.module_loading import import_string


# TODO: Calculate the amount of money

class AbstractLiquidationCalculator(object):
    @staticmethod
    def cal_order_liquidation_amount(order, context=None):
        raise NotImplementedError


class DummyLiquidationCalculator(AbstractLiquidationCalculator):
    @staticmethod
    def cal_order_liquidation_amount(order, context=None):
        return 0


liquidation_calculator = import_string(
    settings.CALCULATOR["LIQUIDATION"]
)  # type: AbstractLiquidationCalculator
